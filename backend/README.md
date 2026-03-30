# Backend API

FastAPI service that receives dataset uploads and runs AI analysis from the `ai` module.

## Run

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## Endpoints

- `GET /api/health`
- `POST /api/analyze` (multipart form)
  - `file`: CSV or Parquet file
  - `title`: dataset title
  - `ipfs_hash`: IPFS hash string
  - `label_col` (optional): label column for class imbalance
