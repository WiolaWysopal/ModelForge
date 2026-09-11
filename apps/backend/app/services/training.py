from dataclasses import dataclass
from sklearn.model_selection import train_test_split

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from app.schemas.training import Algorithm


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

def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric_columns = X.select_dtypes(include="number").columns.tolist()
    categorical_columns = X.select_dtypes(exclude="number").columns.tolist()

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_columns),
            ("categorical", categorical_pipeline, categorical_columns),
        ]
    )


def build_model_pipeline(
    X: pd.DataFrame,
    algorithm: Algorithm,
) -> Pipeline:
    preprocessor = build_preprocessor(X)

    if algorithm == Algorithm.LOGISTIC_REGRESSION:
        model = LogisticRegression(max_iter=1000)

    elif algorithm == Algorithm.RANDOM_FOREST:
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
        )

    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    algorithm: Algorithm,
) -> Pipeline:
    pipeline = build_model_pipeline(
        X=X_train,
        algorithm=algorithm,
    )

    pipeline.fit(X_train, y_train)

    return pipeline