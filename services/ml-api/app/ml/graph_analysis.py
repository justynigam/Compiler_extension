import networkx as nx
import pandas as pd
import json


class GraphAnalyzer:
    def __init__(self):
        self.graph = nx.Graph()

    def build_correlation_graph(
        self, df: pd.DataFrame, threshold: float = 0.5
    ) -> dict:
        corr_matrix = df.corr(numeric_only=True).abs()
        self.graph.clear()
        for i, col_i in enumerate(corr_matrix.columns):
            for j, col_j in enumerate(corr_matrix.columns):
                if i < j and corr_matrix.iloc[i, j] >= threshold:
                    self.graph.add_edge(
                        col_i, col_j, weight=round(corr_matrix.iloc[i, j], 4)
                    )

        return self.get_graph_stats()

    def build_feature_graph(
        self, feature_importances: dict
    ) -> dict:
        self.graph.clear()
        features = list(feature_importances.keys())
        for i, f1 in enumerate(features):
            for j, f2 in enumerate(features):
                if i < j:
                    sim = 1 - abs(
                        feature_importances[f1] - feature_importances[f2]
                    )
                    if sim > 0.3:
                        self.graph.add_edge(f1, f2, weight=round(sim, 4))

        return self.get_graph_stats()

    def get_graph_stats(self) -> dict:
        return {
            "nodes": list(self.graph.nodes()),
            "edges": [
                {"source": u, "target": v, "weight": d["weight"]}
                for u, v, d in self.graph.edges(data=True)
            ],
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
            "density": round(nx.density(self.graph), 4),
            "connected_components": nx.number_connected_components(self.graph),
            "centrality": self._compute_centrality(),
        }

    def _compute_centrality(self) -> dict:
        if self.graph.number_of_nodes() == 0:
            return {}
        try:
            centrality = nx.degree_centrality(self.graph)
            return {k: round(v, 4) for k, v in centrality.items()}
        except Exception:
            return {}

    def export_graph_json(self) -> str:
        stats = self.get_graph_stats()
        return json.dumps(stats, indent=2)