import torch
import shap
import numpy as np
import json


class ModelExplainer:
    def __init__(self):
        self.explainer = None
        self.expected_value = None

    def fit_explainer(self, model, background_data: np.ndarray):
        def predict_fn(x):
            x_tensor = torch.tensor(x, dtype=torch.float32)
            return model.predict_proba(x_tensor).numpy()

        self.explainer = shap.KernelExplainer(
            predict_fn, shap.kmeans(background_data, 50)
        )
        self.expected_value = self.explainer.expected_value
        return self

    def explain(self, input_data: np.ndarray) -> dict:
        if self.explainer is None:
            return {"error": "Explainer not fitted. Call fit_explainer first."}
        shap_values = self.explainer.shap_values(input_data, nsamples=100)
        if isinstance(shap_values, list):
            shap_values = shap_values[0]
        feature_importance = {
            f"feature_{i}": float(abs(shap_values[0][i]))
            for i in range(len(shap_values[0]))
        }
        sorted_importance = dict(
            sorted(
                feature_importance.items(), key=lambda x: x[1], reverse=True
            )
        )
        return {
            "shap_values": shap_values.tolist() if hasattr(shap_values, "tolist") else list(shap_values),
            "feature_importances": sorted_importance,
            "expected_value": (
                self.expected_value.tolist()
                if hasattr(self.expected_value, "tolist")
                else self.expected_value
            ),
        }

    def get_feature_importance(self) -> dict:
        return {
            "message": "Call explain() with input data first"
        }