from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# Add the repository root to Python path so we can import ai.* modules.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai.integration import DatasetRegistryIntegration  # noqa: E402

app = FastAPI(title="DataChain Marketplace API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

integration = DatasetRegistryIntegration()


@app.get("/")
def api_root() -> dict:
    return {
        "name": "DataChain Marketplace API",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "analyze": "/api/analyze",
            "docs": "/docs",
        },
    }


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze")
async def analyze_dataset(
    file: UploadFile = File(...),
    title: str = Form(...),
    ipfs_hash: str = Form(...),
    label_col: Optional[str] = Form(None),
) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing file name")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".csv", ".parquet", ".pq"}:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Use CSV or Parquet.",
        )

    # Save uploaded file to a temp location for analyzer processing.
    temp_path: Optional[str] = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        result = integration.analyze_and_register(
            file_path=temp_path,
            title=title,
            ipfs_hash=ipfs_hash,
            label_col=label_col,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
