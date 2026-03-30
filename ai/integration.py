"""
Integration layer for DatasetRegistry AI analysis
Connects blockchain contract to AI analysis pipeline
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from .analyzer import DatasetAnalyzer
    from .ai_enhanced import AIEnhancedAnalyzer
except ImportError:
    # Support direct execution: python ai/integration.py
    from analyzer import DatasetAnalyzer
    from ai_enhanced import AIEnhancedAnalyzer


class DatasetRegistryIntegration:
    """Integrates dataset analysis with blockchain registry."""

    def __init__(self):
        self.analyzer = DatasetAnalyzer()
        self.ai_enhancer = AIEnhancedAnalyzer()
        self.ai_enhancer.initialize_embeddings()

    def analyze_and_register(
        self, file_path: str, title: str, ipfs_hash: str, label_col: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete pipeline: Analyze dataset -> Generate insights -> Prepare for blockchain
        """
        # Basic analysis
        analysis = self.analyzer.analyze(file_path, label_col)

        if "error" in analysis:
            return analysis

        # AI enhancements
        semantic_desc = self.ai_enhancer.generate_semantic_description(analysis)
        use_cases = self.ai_enhancer.suggest_use_cases_enhanced(analysis)
        embedding = self.ai_enhancer.embed_dataset_description(semantic_desc)

        # Prepare blockchain-ready metadata
        registry_data = {
            "title": title,
            "ipfs_hash": ipfs_hash,
            "analysis": {
                "quality_score": analysis["quality_score"],
                "rows": analysis["rows"],
                "columns": analysis["columns"],
                "tags": analysis["tags"],
            },
            "metadata": {
                "semantic_description": semantic_desc,
                "suggested_use_cases": use_cases,
                "embedding_vector": embedding,  # For semantic search on-chain (future)
            },
            "raw_analysis": analysis,
        }

        return registry_data


# Example: How the AI layer connects to blockchain
if __name__ == "__main__":
    integration = DatasetRegistryIntegration()

    # Simulate dataset upload
    sample_data = {
        "patient_id": list(range(1, 1001)),
        "age": [25 + i % 50 for i in range(1000)],
        "disease_indicator": ["yes", "no"] * 500,
        "treatment": ["A", "B", "C"] * 333 + ["A"],
    }

    import pandas as pd

    df = pd.DataFrame(sample_data)
    test_file = "health_dataset.csv"
    df.to_csv(test_file, index=False)

    # Full analysis and registration preparation
    result = integration.analyze_and_register(
        file_path=test_file,
        title="Health Dataset - Disease Prediction",
        ipfs_hash="QmExampleHash123",
        label_col="disease_indicator",
    )

    print(json.dumps(result, indent=2, default=str))

    # Cleanup
    Path(test_file).unlink()
