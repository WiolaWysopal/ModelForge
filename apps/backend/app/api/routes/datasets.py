from pathlib import Path
from uuid import uuid4
import pandas as pd

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.dataset import Dataset

from app.schemas.dataset import DatasetPreviewResponse, DatasetResponse

from app.core.config import settings

router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"],
)


UPLOAD_DIR = Path("data/datasets")


@router.post("/upload", response_model=DatasetResponse)
def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if file.filename is None or Path(file.filename).suffix.lower() != ".csv":
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed.",
        )
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    max_size_bytes = settings.max_upload_size_mb * 1024 * 1024

    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File is too large. Maximum size is {settings.max_upload_size_mb} MB.",
        )
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_extension = Path(file.filename).suffix
    stored_filename = f"{uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / stored_filename

    with file_path.open("wb") as destination:
        destination.write(file.file.read())

    dataframe = pd.read_csv(file_path)

    row_count = len(dataframe)
    column_count = len(dataframe.columns)
    missing_values_count = int(dataframe.isna().sum().sum())

    dataset = Dataset(
        filename=file.filename,
        file_path=str(file_path),
        row_count=row_count,
        column_count=column_count,
        missing_values_count=missing_values_count,
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset

@router.get("/{dataset_id}/preview", response_model=DatasetPreviewResponse)
def preview_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
):
    dataset = db.get(Dataset, dataset_id)

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found.",
        )

    dataframe = pd.read_csv(dataset.file_path)

    preview = dataframe.head(5)

    return {
        "dataset_id": dataset.id,
        "filename": dataset.filename,
        "columns": preview.columns.tolist(),
        "rows": preview.to_dict(orient="records"),
    }