from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split


@dataclass
class TrainingData:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def prepare_training_data(
    dataframe: pd.DataFrame,
    target_column: str,
    test_size: float,
    random_state: int = 42,
) -> TrainingData:
    if target_column not in dataframe.columns:
        raise ValueError(f"Target column '{target_column}' does not exist.")

    X = dataframe.drop(columns=[target_column])
    y = dataframe[target_column]

    if X.empty:
        raise ValueError("Dataset must contain at least one feature column.")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
    )

    return TrainingData(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
    )