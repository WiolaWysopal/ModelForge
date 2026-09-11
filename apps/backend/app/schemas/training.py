from enum import StrEnum

from pydantic import BaseModel, Field


class Algorithm(StrEnum):
    LOGISTIC_REGRESSION = "logistic_regression"
    RANDOM_FOREST = "random_forest"


class TrainingRequest(BaseModel):
    dataset_id: int
    target_column: str
    algorithm: Algorithm
    test_size: float = Field(default=0.2, gt=0, lt=1)


class TrainingResponse(BaseModel):
    dataset_id: int
    target_column: str
    algorithm: Algorithm
    test_size: float
    train_size: int
    test_size_rows: int
    model_path: str