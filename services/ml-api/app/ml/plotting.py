import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import base64
from io import BytesIO


class ChartGenerator:
    @staticmethod
    def feature_importance_chart(feature_importances: dict) -> str:
        features = list(feature_importances.keys())
        values = list(feature_importances.values())
        fig = go.Figure(
            go.Bar(
                x=values,
                y=features,
                orientation="h",
                marker=dict(
                    color=values,
                    colorscale="Viridis",
                    showscale=True,
                ),
            )
        )
        fig.update_layout(
            title="Feature Importances (SHAP)",
            xaxis_title="Importance",
            yaxis_title="Features",
            template="plotly_dark",
            height=max(400, len(features) * 25),
        )
        return ChartGenerator._fig_to_json(fig)

    @staticmethod
    def training_history_chart(history: dict) -> str:
        fig = go.Figure()
        if "train_loss" in history:
            fig.add_trace(
                go.Scatter(
                    y=history["train_loss"],
                    mode="lines+markers",
                    name="Train Loss",
                    line=dict(color="#636EFA"),
                )
            )
        if "val_loss" in history:
            fig.add_trace(
                go.Scatter(
                    y=history["val_loss"],
                    mode="lines+markers",
                    name="Val Loss",
                    line=dict(color="#EF553B"),
                )
            )
        if "train_accuracy" in history:
            fig.add_trace(
                go.Scatter(
                    y=history["train_accuracy"],
                    mode="lines+markers",
                    name="Train Accuracy",
                    line=dict(color="#00CC96"),
                    yaxis="y2",
                )
            )
        fig.update_layout(
            title="Training History",
            xaxis_title="Epoch",
            yaxis_title="Loss",
            yaxis2=dict(title="Accuracy", overlaying="y", side="right"),
            template="plotly_dark",
            hovermode="x unified",
        )
        return ChartGenerator._fig_to_json(fig)

    @staticmethod
    def correlation_heatmap(df: pd.DataFrame) -> str:
        corr = df.corr(numeric_only=True)
        fig = go.Figure(
            go.Heatmap(
                z=corr.values,
                x=corr.columns.tolist(),
                y=corr.columns.tolist(),
                colorscale="RdBu",
                zmin=-1,
                zmax=1,
                text=[[f"{v:.2f}" for v in row] for row in corr.values],
                texttemplate="%{text}",
            )
        )
        fig.update_layout(
            title="Correlation Heatmap",
            template="plotly_dark",
            height=600,
            width=800,
        )
        return ChartGenerator._fig_to_json(fig)

    @staticmethod
    def graph_visualization(graph_stats: dict) -> str:
        fig = go.Figure()
        x_positions = {}
        y_positions = {}
        nodes = graph_stats.get("nodes", [])
        for i, node in enumerate(nodes):
            angle = 2 * np.pi * i / len(nodes) if nodes else 0
            x_positions[node] = np.cos(angle)
            y_positions[node] = np.sin(angle)

        for edge in graph_stats.get("edges", []):
            fig.add_trace(
                go.Scatter(
                    x=[x_positions[edge["source"]], x_positions[edge["target"]]],
                    y=[y_positions[edge["source"]], y_positions[edge["target"]]],
                    mode="lines",
                    line=dict(width=edge.get("weight", 1) * 3, color="#888"),
                    hoverinfo="text",
                    text=f"Weight: {edge.get('weight', 'N/A')}",
                    showlegend=False,
                )
            )
        centrality = graph_stats.get("centrality", {})
        if nodes:
            sizes = [max(5, centrality.get(n, 0.1) * 50) for n in nodes]
            labels = [f"{n}<br>Centrality: {centrality.get(n, 0):.3f}" for n in nodes]
            fig.add_trace(
                go.Scatter(
                    x=[x_positions[n] for n in nodes],
                    y=[y_positions[n] for n in nodes],
                    mode="markers+text",
                    text=nodes,
                    textposition="top center",
                    marker=dict(
                        size=sizes,
                        color=list(range(len(nodes))),
                        colorscale="Viridis",
                        showscale=True,
                        colorbar=dict(title="Node Index"),
                    ),
                    hovertext=labels,
                    showlegend=False,
                )
            )
        fig.update_layout(
            title="Feature Relationship Network Graph",
            template="plotly_dark",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600,
        )
        return ChartGenerator._fig_to_json(fig)

    @staticmethod
    def prediction_distribution(predictions: list[dict]) -> str:
        if not predictions:
            return json.dumps({"data": [], "layout": {}})
        classes = [p["prediction"] for p in predictions]
        confidences = [p.get("confidence", 0) for p in predictions]
        class_counts = {}
        for cls in classes:
            class_counts[cls] = class_counts.get(cls, 0) + 1
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=list(class_counts.keys()),
                y=list(class_counts.values()),
                name="Count",
                marker_color="#636EFA",
                yaxis="y",
            )
        )
        if confidences:
            fig.add_trace(
                go.Box(
                    y=confidences,
                    name="Confidence",
                    marker_color="#EF553B",
                    yaxis="y2",
                )
            )
        fig.update_layout(
            title="Prediction Distribution",
            template="plotly_dark",
            yaxis=dict(title="Count"),
            yaxis2=dict(title="Confidence", overlaying="y", side="right"),
        )
        return ChartGenerator._fig_to_json(fig)

    @staticmethod
    def _fig_to_json(fig: go.Figure) -> str:
        return json.dumps(json.loads(fig.to_json()))


graph_data = []