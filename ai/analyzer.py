"""
DatasetRegistry AI Analyzer
Automated quality scoring and semantic analysis for datasets
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import Counter


class DatasetAnalyzer:
    """Analyzes dataset quality, schema, and generates intelligent insights."""

    def __init__(self):
        self.df = None
        self.file_path = None

    def load_dataset(self, file_path: str) -> bool:
        """Load CSV or Parquet dataset."""
        try:
            path = Path(file_path)
            if path.suffix == ".csv":
                self.df = pd.read_csv(file_path)
            elif path.suffix in [".parquet", ".pq"]:
                self.df = pd.read_parquet(file_path)
            else:
                raise ValueError("Supported formats: CSV, Parquet")
            self.file_path = file_path
            return True
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return False

    def get_basic_stats(self) -> Dict[str, Any]:
        """Extract basic dataset statistics."""
        if self.df is None:
            return {}

        rows, cols = self.df.shape
        missing_values = self.df.isnull().sum()
        missing_percentage = (missing_values.sum() / (rows * cols)) * 100

        column_types = {}
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            if "int" in dtype:
                column_types[col] = "numeric"
            elif "float" in dtype:
                column_types[col] = "numeric"
            elif "object" in dtype:
                column_types[col] = "categorical"
            elif "datetime" in dtype:
                column_types[col] = "datetime"
            else:
                column_types[col] = "other"

        return {
            "rows": rows,
            "columns": cols,
            "missing_percentage": round(missing_percentage, 2),
            "column_types": column_types,
            "column_count_by_type": self._count_by_type(column_types),
        }

    def detect_class_imbalance(self, label_col: Optional[str] = None) -> Dict[str, Any]:
        """Detect class imbalance if a label column exists."""
        if self.df is None or label_col is None:
            return {"detected": False}

        if label_col not in self.df.columns:
            return {"detected": False, "reason": f"Column '{label_col}' not found"}

        try:
            value_counts = self.df[label_col].value_counts()
            total = len(self.df)

            # Calculate imbalance ratio
            counts_dict = value_counts.to_dict()
            max_count = value_counts.max()
            min_count = value_counts.min()
            imbalance_ratio = max_count / min_count if min_count > 0 else float("inf")

            # Percentages
            class_distribution = {
                str(k): round((v / total) * 100, 2) for k, v in counts_dict.items()
            }

            return {
                "detected": True,
                "label_column": label_col,
                "class_distribution": class_distribution,
                "imbalance_ratio": round(imbalance_ratio, 2),
                "is_imbalanced": imbalance_ratio > 1.5,
            }
        except Exception as e:
            return {"detected": False, "error": str(e)}

    def calculate_quality_score(self, label_col: Optional[str] = None) -> float:
        """Calculate overall dataset quality score (0-100)."""
        if self.df is None:
            return 0

        score = 100.0

        # Penalize missing values
        stats = self.get_basic_stats()
        missing_pct = stats.get("missing_percentage", 0)
        score -= missing_pct * 0.5  # Up to 50 points

        # Penalize size if too small
        rows = stats.get("rows", 0)
        if rows < 100:
            score -= 20
        elif rows < 1000:
            score -= 10

        # Penalize imbalance
        imbalance = self.detect_class_imbalance(label_col)
        if imbalance.get("is_imbalanced"):
            ratio = imbalance.get("imbalance_ratio", 1)
            score -= min(15, ratio * 5)  # Up to 15 points

        return max(0, min(100, round(score, 1)))

    def infer_tags(self, label_col: Optional[str] = None) -> List[str]:
        """Infer dataset tags based on structure and content."""
        tags = []

        if self.df is None:
            return tags

        stats = self.get_basic_stats()
        col_types = stats.get("column_types", {})

        # Tag by size
        rows = stats.get("rows", 0)
        if rows > 100000:
            tags.append("large-scale")
        elif rows > 10000:
            tags.append("medium")
        else:
            tags.append("small")

        # Tag by column composition
        numeric_count = sum(1 for t in col_types.values() if t == "numeric")
        cat_count = sum(1 for t in col_types.values() if t == "categorical")

        if numeric_count > cat_count:
            tags.append("numeric-heavy")
        elif cat_count > numeric_count:
            tags.append("categorical-heavy")

        # Tag by task type
        imbalance = self.detect_class_imbalance(label_col)
        if imbalance.get("detected"):
            if imbalance.get("imbalance_ratio", 1) > 1.5:
                tags.append("imbalanced")
            else:
                tags.append("balanced")

        # Tag by quality
        quality = self.calculate_quality_score(label_col)
        if quality > 80:
            tags.append("high-quality")
        elif quality > 50:
            tags.append("moderate-quality")
        else:
            tags.append("low-quality")

        # Tag by completeness
        missing_pct = stats.get("missing_percentage", 0)
        if missing_pct < 1:
            tags.append("complete")
        elif missing_pct < 10:
            tags.append("mostly-complete")

        return list(set(tags))

    def analyze(
        self, file_path: str, label_col: Optional[str] = None
    ) -> Dict[str, Any]:
        """Run full analysis pipeline."""
        if not self.load_dataset(file_path):
            return {"error": "Failed to load dataset"}

        stats = self.get_basic_stats()
        imbalance = self.detect_class_imbalance(label_col)
        quality = self.calculate_quality_score(label_col)
        tags = self.infer_tags(label_col)

        return {
            "file_path": file_path,
            "rows": stats["rows"],
            "columns": stats["columns"],
            "missing_percentage": stats["missing_percentage"],
            "column_types": stats["column_types"],
            "quality_score": quality,
            "imbalance_analysis": imbalance,
            "tags": tags,
            "statistics": {
                "numeric_columns": stats["column_count_by_type"].get("numeric", 0),
                "categorical_columns": stats["column_count_by_type"].get("categorical", 0),
                "datetime_columns": stats["column_count_by_type"].get("datetime", 0),
            },
        }

    def generate_description(self) -> str:
        """Generate simple dataset description (v1 - AI enhancement coming)."""
        if self.df is None:
            return ""

        stats = self.get_basic_stats()
        rows = stats["rows"]
        cols = stats["columns"]
        missing = stats["missing_percentage"]

        description = f"This dataset contains {rows} rows and {cols} columns. "
        description += f"Completeness: {100 - missing:.1f}%. "

        return description

    def suggest_use_cases(self) -> List[str]:
        """Suggest ML use cases based on dataset structure (v1)."""
        suggestions = []

        if self.df is None:
            return suggestions

        # Placeholder for AI-enhanced suggestions
        # Will be upgraded with LLM + Hugging Face

        return [
            "Classification tasks",
            "Exploratory data analysis",
            "Statistical analysis",
        ]

    @staticmethod
    def _count_by_type(column_types: Dict[str, str]) -> Dict[str, int]:
        """Count columns by type."""
        counts = Counter(column_types.values())
        return dict(counts)


# Example usage
if __name__ == "__main__":
    analyzer = DatasetAnalyzer()

    # Create a sample dataset for testing
    sample_data = {
        "age": [25, 30, 35, 40, 45] * 200,
        "income": [50000, 60000, 70000, 80000, 90000] * 200,
        "employed": ["yes", "no", "yes", "yes", "no"] * 200,
        "city": ["NYC", "LA", "Chicago", "Houston", "Phoenix"] * 200,
    }
    sample_df = pd.DataFrame(sample_data)
    sample_df.loc[::10, "income"] = np.nan  # Add some missing values
    sample_file = "sample_dataset.csv"
    sample_df.to_csv(sample_file, index=False)

    # Run analysis
    result = analyzer.analyze(sample_file, label_col="employed")
    print(json.dumps(result, indent=2))

    # Cleanup
    Path(sample_file).unlink()
