import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.dataset import Dataset
from app.schemas.training import TrainingRequest, TrainingResponse
from app.services.training import (
    prepare_training_data,
    save_model,
    train_model,
)

router = APIRouter(prefix="/training", tags=["Training"])


@router.post(
    "",
    response_model=TrainingResponse,
    status_code=status.HTTP_201_CREATED,
)
def train(
    request: TrainingRequest,
    db: Session = Depends(get_db),
) -> TrainingResponse:
    dataset = db.get(Dataset, request.dataset_id)

    if dataset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found.",
        )

    try:
        dataframe = pd.read_csv(dataset.file_path)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset file not found.",
        )

    try:
        training_data = prepare_training_data(
            dataframe=dataframe,
            target_column=request.target_column,
            test_size=request.test_size,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        )

    pipeline = train_model(
        X_train=training_data.X_train,
        y_train=training_data.y_train,
        algorithm=request.algorithm,
    )

    model_path = save_model(pipeline)

    return TrainingResponse(
        dataset_id=request.dataset_id,
        target_column=request.target_column,
        algorithm=request.algorithm,
        test_size=request.test_size,
        train_size=len(training_data.X_train),
        test_size_rows=len(training_data.X_test),
        model_path=model_path,
    )