import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from app.ml.transformer_model import TransformerClassifier


class ModelTrainer:
    def __init__(self, device: str | None = None):
        self.device = (
            torch.device(device)
            if device
            else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.history = {
            "train_loss": [],
            "val_loss": [],
            "train_accuracy": [],
            "val_accuracy": [],
        }

    def load_and_preprocess(
        self, file_path: str, target_column: str
    ) -> tuple[np.ndarray, np.ndarray]:
        df = pd.read_csv(file_path)
        y = df[target_column]
        X = df.drop(columns=[target_column])
        X = pd.get_dummies(X, drop_first=True)
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        self.feature_names = X.columns.tolist()
        return X_scaled, y_encoded

    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
        epochs: int = 10,
        batch_size: int = 32,
        lr: float = 1e-3,
        val_split: float = 0.2,
    ) -> dict:
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=val_split, stratify=y, random_state=42
        )
        X_train_t = torch.tensor(X_train, dtype=torch.float32)
        y_train_t = torch.tensor(y_train, dtype=torch.long)
        X_val_t = torch.tensor(X_val, dtype=torch.float32)
        y_val_t = torch.tensor(y_val, dtype=torch.long)

        input_dim = X.shape[1]
        num_classes = len(set(y))

        self.model = TransformerClassifier(
            input_dim=input_dim, num_classes=num_classes
        ).to(self.device)

        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=lr)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=epochs
        )

        history = {
            "train_loss": [],
            "val_loss": [],
            "train_accuracy": [],
            "val_accuracy": [],
        }

        for epoch in range(epochs):
            self.model.train()
            total_loss = 0
            correct = 0
            total = 0
            for i in range(0, len(X_train_t), batch_size):
                X_batch = X_train_t[i : i + batch_size].to(self.device)
                y_batch = y_train_t[i : i + batch_size].to(self.device)
                optimizer.zero_grad()
                logits = self.model(X_batch)
                loss = criterion(logits, y_batch)
                loss.backward()
                optimizer.step()
                total_loss += loss.item() * len(X_batch)
                preds = logits.argmax(dim=1)
                correct += (preds == y_batch).sum().item()
                total += len(X_batch)
            scheduler.step()
            train_loss = total_loss / total
            train_acc = correct / total
            history["train_loss"].append(round(train_loss, 4))
            history["train_accuracy"].append(round(train_acc, 4))

            # ----- validation -----
            self.model.eval()
            with torch.no_grad():
                X_val_d = X_val_t.to(self.device)
                y_val_d = y_val_t.to(self.device)
                logits = self.model(X_val_d)
                val_loss = criterion(logits, y_val_d).item()
                preds = logits.argmax(dim=1)
                val_acc = (preds == y_val_d).sum().item() / len(y_val_d)
            history["val_loss"].append(round(val_loss, 4))
            history["val_accuracy"].append(round(val_acc, 4))

        self.history = history
        accuracy = history["val_accuracy"][-1]
        num_correct = int(round(accuracy * len(y_val)))
        total_samples = len(y_val)
        val_preds = (
            self.model(X_val_t.to(self.device)).argmax(dim=1).cpu().numpy()
        )
        f1 = self._compute_f1(y_val, val_preds)
        return {
            "history": history,
            "accuracy": round(accuracy, 4),
            "f1_score": round(f1, 4),
            "input_dim": X.shape[1],
            "num_classes": num_classes,
            "feature_names": self.feature_names,
            "device": str(self.device),
        }

    def predict(self, X: np.ndarray) -> dict:
        if self.model is None:
            return {"error": "Model not trained"}
        if self.scaler is not None:
            X = self.scaler.transform(X)
        X_t = torch.tensor(X, dtype=torch.float32).to(self.device)
        self.model.eval()
        with torch.no_grad():
            logits = self.model(X_t)
            probs = torch.softmax(logits, dim=-1)
            preds = logits.argmax(dim=-1)
            confidences = probs.max(dim=-1).values
        pred_labels = (
            self.label_encoder.inverse_transform(preds.cpu().numpy())
            if self.label_encoder
            else preds.cpu().numpy().tolist()
        )
        return {
            "predictions": pred_labels,
            "confidences": confidences.cpu().numpy().tolist(),
            "probabilities": probs.cpu().numpy().tolist(),
        }

    def get_model(self):
        return self.model

    def save_model(self, path: str):
        if self.model:
            torch.save(
                {
                    "model_state_dict": self.model.state_dict(),
                    "scaler": self.scaler,
                    "label_encoder": self.label_encoder,
                    "feature_names": self.feature_names,
                    "history": self.history,
                },
                path,
            )

    def load_model(self, path: str):
        checkpoint = torch.load(path, map_location=self.device, weights_only=False)
        self.scaler = checkpoint["scaler"]
        self.label_encoder = checkpoint["label_encoder"]
        self.feature_names = checkpoint["feature_names"]
        self.history = checkpoint.get("history", {})
        input_dim = self.scaler.n_features_in_
        num_classes = len(self.label_encoder.classes_)
        self.model = TransformerClassifier(
            input_dim=input_dim, num_classes=num_classes
        ).to(self.device)
        self.model.load_state_dict(checkpoint["model_state_dict"])

    def _compute_f1(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        from sklearn.metrics import f1_score
        return f1_score(y_true, y_pred, average="weighted")