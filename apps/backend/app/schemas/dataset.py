from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DatasetResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    row_count: int
    column_count: int
    missing_values_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)