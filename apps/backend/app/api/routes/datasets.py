from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.dataset import Dataset

from app.schemas.dataset import DatasetResponse


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
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_extension = Path(file.filename).suffix
    stored_filename = f"{uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / stored_filename

    with file_path.open("wb") as destination:
        destination.write(file.file.read())

    dataset = Dataset(
        filename=file.filename,
        file_path=str(file_path),
        row_count=0,
        column_count=0,
        missing_values_count=0,
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset