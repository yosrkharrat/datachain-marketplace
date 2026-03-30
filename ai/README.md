# AI Layer — Dataset Analysis & Quality Scoring

This module provides automated dataset analysis and quality scoring for the DatasetRegistry marketplace.

## Features

### v1: Core Analysis
- **Dataset profiling**: rows, columns, data types (numeric, categorical, datetime)
- **Missing value detection**: percentage of missing data with per-column breakdown
- **Class imbalance detection**: identifies imbalanced datasets (useful for ML teams)
- **Quality scoring**: algorithmic quality assessment (0-100 scale)
- **Automatic tagging**: intelligent dataset classification (size, quality, imbalance)

### v2: AI-Enhanced (in development)
- **Semantic descriptions**: Hugging Face embeddings for natural language search
- **Intelligent use-case suggestions**: recommends ML tasks (classification, clustering, regression, anomaly detection)
- **Similarity search**: find semantically similar datasets with `"Find health data for disease classification"`
- **Bias detection**: placeholder for fairness analysis
- **Dataset embeddings**: enable semantic search directly from blockchain

## Installation

```bash
cd ai
pip install -r requirements.txt
```

Optional (for AI features):
```bash
pip install transformers sentence-transformers torch
```

## Usage

### Basic Analysis
```python
from analyzer import DatasetAnalyzer

analyzer = DatasetAnalyzer()
result = analyzer.analyze("my_dataset.csv", label_col="target")

print(result)
# Output:
# {
#   "rows": 12000,
#   "columns": 15,
#   "missing_percentage": 2.3,
#   "quality_score": 78,
#   "tags": ["medium", "numeric-heavy", "high-quality"],
#   ...
# }
```

### AI-Enhanced Analysis with Blockchain Integration
```python
from integration import DatasetRegistryIntegration

integration = DatasetRegistryIntegration()
registry_data = integration.analyze_and_register(
    file_path="dataset.csv",
    title="Health Dataset",
    ipfs_hash="QmHash...",
    label_col="disease"
)

# Now ready to register on blockchain with:
# - quality_score (immutable)
# - semantic_description (AI-generated)
# - use_case suggestions
# - embedding vector (for decentralized semantic search)
```

### Semantic Search
```python
from ai_enhanced import AIEnhancedAnalyzer

enhancer = AIEnhancedAnalyzer()
enhancer.initialize_embeddings()

query = "dataset suitable for disease prediction and medical classification"
similar = enhancer.find_similar_datasets(query, dataset_embeddings_list)

# Returns top 5 dataset matches by semantic similarity
```

## Quality Score Calculation

Quality score (0-100) considers:
- **Completeness**: Missing values penalty
- **Size**: Small datasets penalized
- **Class balance**: Imbalanced datasets flagged
- **Data types**: Diverse features rewarded

Example:
- 100,000 rows, 2% missing, balanced → Score: ~95
- 500 rows, 20% missing, imbalanced → Score: ~45

## Tags Generated

Datasets are automatically tagged with:
- Size: `small`, `medium`, `large-scale`
- Content: `numeric-heavy`, `categorical-heavy`
- Quality: `high-quality`, `moderate-quality`, `low-quality`
- Completeness: `complete`, `mostly-complete`
- Balance: `balanced`, `imbalanced`

## Architecture

```
analyzer.py
  ↓ (basic stats, quality score)
integration.py ← ai_enhanced.py
  ↓ (semantic descriptions, embeddings)
DatasetRegistry (blockchain)
  ↓ (immutable quality record + AI insights)
Marketplace frontend
  ↓ (users search & discover trusted datasets)
```

## Future Enhancements

- [ ] LLM-based dataset description generation (Claude/GPT-4)
- [ ] Fairness 360 integration for bias detection
- [ ] Column-level semantic embeddings
- [ ] Outlier and anomaly detection
- [ ] Automated data profiling reports
- [ ] Schema matching across datasets

## Contributing

Quality analysis is critical to marketplace trust. PRs welcome for:
- Additional quality metrics
- Improved tag inference
- Performance optimizations
- LLM integration examples

---

**Why this matters**: On platforms like Kaggle, finding trustworthy, quality datasets is painful. This AI layer provides the **signal** that blockchain provides the **immutability** for. Together, they create marketplace advantage.
