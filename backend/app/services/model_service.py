import os
import json
import torch
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from app.models.model import MLModel as MLModelORM
from app.ml.training import ModelTrainer
from app.ml.explainability import ModelExplainer
from app.ml.graph_analysis import GraphAnalyzer
from app.ml.plotting import ChartGenerator
from app.core.redis_queue import task_queue
from app.services.dataset_service import DatasetService


MODEL_DIR = "./saved_models"
os.makedirs(MODEL_DIR, exist_ok=True)

_active_trainers: dict[int, ModelTrainer] = {}
_active_explainers: dict[int, ModelExplainer] = {}


class ModelService:
    @classmethod
    async def create_model(
        cls,
        db: AsyncSession,
        name: str,
        model_type: str,
        description: str | None,
        config: str | None,
    ) -> MLModelORM:
        model = MLModelORM(
            name=name,
            model_type=model_type,
            description=description,
            config=config,
        )
        db.add(model)
        await db.flush()
        return model

    @classmethod
    async def get_model(cls, db: AsyncSession, model_id: int) -> MLModelORM | None:
        result = await db.execute(
            select(MLModelORM).where(MLModelORM.id == model_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def list_models(
        cls, db: AsyncSession, skip: int = 0, limit: int = 50
    ) -> tuple[list[MLModelORM], int]:
        from sqlalchemy import func as sqlfunc
        count_q = await db.execute(select(sqlfunc.count(MLModelORM.id)))
        total = count_q.scalar()
        result = await db.execute(
            select(MLModelORM)
            .offset(skip)
            .limit(limit)
            .order_by(MLModelORM.created_at.desc())
        )
        return result.scalars().all(), total

    @classmethod
    async def train_model(
        cls,
        db: AsyncSession,
        model_id: int,
        dataset_id: int,
        target_column: str,
        epochs: int = 10,
    ) -> dict:
        model_orm = await cls.get_model(db, model_id)
        dataset = await DatasetService.get_dataset(db, dataset_id)
        if not model_orm or not dataset:
            return {"error": "Model or dataset not found"}

        trainer = ModelTrainer()
        X, y = trainer.load_and_preprocess(dataset.file_path, target_column)
        result = trainer.train(X, y, epochs=epochs)

        artifact_path = os.path.join(MODEL_DIR, f"model_{model_id}.pt")
        trainer.save_model(artifact_path)

        model_orm.artifact_path = artifact_path
        model_orm.accuracy = result["accuracy"]
        model_orm.f1_score = result["f1_score"]
        model_orm.status = "trained"
        model_orm.config = json.dumps(
            {
                "input_dim": result["input_dim"],
                "num_classes": result["num_classes"],
                "feature_names": result["feature_names"],
            }
        )

        _active_trainers[model_id] = trainer
        await db.flush()

        # generate charts
        charts = {
            "training_history": ChartGenerator.training_history_chart(result["history"]),
        }
        df = pd.read_csv(dataset.file_path)
        charts["correlation_heatmap"] = ChartGenerator.correlation_heatmap(df)

        return {
            "model_id": model_id,
            "accuracy": result["accuracy"],
            "f1_score": result["f1_score"],
            "history": result["history"],
            "charts": charts,
        }

    @classmethod
    async def predict(
        cls, db: AsyncSession, model_id: int, inputs: dict
    ) -> dict:
        trainer = _active_trainers.get(model_id)
        if trainer is None:
            model_orm = await cls.get_model(db, model_id)
            if not model_orm or not model_orm.artifact_path:
                return {"error": "Model not trained"}
            trainer = ModelTrainer()
            trainer.load_model(model_orm.artifact_path)
            _active_trainers[model_id] = trainer

        import pandas as pd
        import numpy as np

        input_df = pd.DataFrame([inputs])
        all_features = trainer.feature_names
        for col in all_features:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = pd.get_dummies(input_df, drop_first=True)
        for col in all_features:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[all_features]
        X = input_df.values.astype(np.float32)
        result = trainer.predict(X)
        return {
            "predictions": result["predictions"][0] if result["predictions"] else None,
            "confidence": (
                result["confidences"][0] if result["confidences"] else None
            ),
            "probabilities": (
                result["probabilities"][0] if result["probabilities"] else None
            ),
        }

    @classmethod
    async def explain(
        cls, db: AsyncSession, model_id: int, inputs: dict
    ) -> dict:
        model_orm = await cls.get_model(db, model_id)
        if not model_orm or not model_orm.artifact_path:
            return {"error": "Model not trained"}

        trainer = _active_trainers.get(model_id)
        if trainer is None:
            trainer = ModelTrainer()
            trainer.load_model(model_orm.artifact_path)
            _active_trainers[model_id] = trainer

        dataset = await DatasetService.get_dataset(
            db, 1
        )

        import pandas as pd
        import numpy as np

        input_df = pd.DataFrame([inputs])
        all_features = trainer.feature_names
        for col in all_features:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = pd.get_dummies(input_df, drop_first=True)
        for col in all_features:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[all_features]
        X_sample = input_df.values.astype(np.float32)

        background = np.random.randn(50, X_sample.shape[1]).astype(np.float32)
        if dataset:
            try:
                df_bg = pd.read_csv(dataset.file_path)
                for col in all_features:
                    if col not in df_bg.columns:
                        df_bg[col] = 0
                df_bg = pd.get_dummies(df_bg, drop_first=True)
                for col in all_features:
                    if col not in df_bg.columns:
                        df_bg[col] = 0
                df_bg = df_bg[all_features]
                background = df_bg.sample(min(50, len(df_bg))).values.astype(np.float32)
            except Exception:
                pass

        explainer = ModelExplainer()
        explainer.fit_explainer(trainer.get_model(), background)
        explanation = explainer.explain(X_sample)

        explain_chart = ChartGenerator.feature_importance_chart(
            explanation["feature_importances"]
        )

        return {
            "feature_importances": explanation["feature_importances"],
            "shap_values": explanation.get("shap_values"),
            "expected_value": explanation.get("expected_value"),
            "chart": explain_chart,
        }

    @classmethod
    async def analyze_graph(
        cls, db: AsyncSession, model_id: int
    ) -> dict:
        model_orm = await cls.get_model(db, model_id)
        if not model_orm or not model_orm.config:
            return {"error": "Model config not found"}
        config = json.loads(model_orm.config) if isinstance(model_orm.config, str) else model_orm.config
        feature_names = config.get("feature_names", [])
        accuracy = model_orm.accuracy or 0.5
        importances = {
            name: accuracy * (0.5 + 0.5 * (i % 3) / 3)
            for i, name in enumerate(feature_names)
        } if feature_names else {}
        analyzer = GraphAnalyzer()
        graph_stats = analyzer.build_feature_graph(
            importances
        )
        chart = ChartGenerator.graph_visualization(graph_stats)
        return {
            "graph_stats": graph_stats,
            "chart": chart,
        }

    @classmethod
    async def delete_model(cls, db: AsyncSession, model_id: int) -> bool:
        model = await cls.get_model(db, model_id)
        if not model:
            return False
        if model.artifact_path and os.path.exists(model.artifact_path):
            os.remove(model.artifact_path)
        _active_trainers.pop(model_id, None)
        _active_explainers.pop(model_id, None)
        await db.delete(model)
        return True