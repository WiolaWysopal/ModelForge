from pathlib import Path
import pandas as pd
import pytest

from app.services.training import (
    build_model_pipeline,
    prepare_training_data,
    save_model,
    train_model,
)

def test_prepare_training_data_splits_dataset():
    dataframe = pd.DataFrame(
        {
            "feature_a": range(10),
            "feature_b": range(10, 20),
            "target": [0, 1] * 5,
        }
    )

    result = prepare_training_data(
        dataframe=dataframe,
        target_column="target",
        test_size=0.2,
    )

    assert len(result.X_train) == 8
    assert len(result.X_test) == 2
    assert len(result.y_train) == 8
    assert len(result.y_test) == 2


def test_prepare_training_data_removes_target_from_features():
    dataframe = pd.DataFrame(
        {
            "feature": range(10),
            "target": [0, 1] * 5,
        }
    )

    result = prepare_training_data(
        dataframe=dataframe,
        target_column="target",
        test_size=0.2,
    )

    assert "target" not in result.X_train.columns
    assert "target" not in result.X_test.columns


def test_prepare_training_data_rejects_missing_target_column():
    dataframe = pd.DataFrame(
        {
            "feature": range(10),
            "target": [0, 1] * 5,
        }
    )

    with pytest.raises(ValueError, match="Target column"):
        prepare_training_data(
            dataframe=dataframe,
            target_column="missing",
            test_size=0.2,
        )


def test_prepare_training_data_rejects_dataset_without_features():
    dataframe = pd.DataFrame(
        {
            "target": [0, 1] * 5,
        }
    )

    with pytest.raises(ValueError, match="feature column"):
        prepare_training_data(
            dataframe=dataframe,
            target_column="target",
            test_size=0.2,
        )

from sklearn.pipeline import Pipeline

from app.schemas.training import Algorithm
from app.services.training import build_model_pipeline


def test_build_model_pipeline_for_logistic_regression():
    dataframe = pd.DataFrame(
        {
            "age": [20, 30, 40],
            "city": ["Krakow", "Warsaw", "Krakow"],
        }
    )

    pipeline = build_model_pipeline(
        X=dataframe,
        algorithm=Algorithm.LOGISTIC_REGRESSION,
    )

    assert isinstance(pipeline, Pipeline)
    assert "preprocessor" in pipeline.named_steps
    assert "model" in pipeline.named_steps
    assert pipeline.named_steps["model"].__class__.__name__ == "LogisticRegression"


def test_build_model_pipeline_for_random_forest():
    dataframe = pd.DataFrame(
        {
            "age": [20, 30, 40],
            "city": ["Krakow", "Warsaw", "Krakow"],
        }
    )

    pipeline = build_model_pipeline(
        X=dataframe,
        algorithm=Algorithm.RANDOM_FOREST,
    )

    assert isinstance(pipeline, Pipeline)
    assert pipeline.named_steps["model"].__class__.__name__ == "RandomForestClassifier"

def test_train_model_returns_fitted_pipeline():
    dataframe = pd.DataFrame(
        {
            "age": [20, 22, 25, 28, 30, 35, 40, 45, 50, 55],
            "city": [
                "Krakow",
                "Warsaw",
                "Krakow",
                "Warsaw",
                "Krakow",
                "Warsaw",
                "Krakow",
                "Warsaw",
                "Krakow",
                "Warsaw",
            ],
            "target": [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        }
    )

    training_data = prepare_training_data(
        dataframe=dataframe,
        target_column="target",
        test_size=0.2,
    )

    pipeline = train_model(
        X_train=training_data.X_train,
        y_train=training_data.y_train,
        algorithm=Algorithm.RANDOM_FOREST,
    )

    predictions = pipeline.predict(training_data.X_test)

    assert isinstance(pipeline, Pipeline)
    assert len(predictions) == len(training_data.X_test)

def test_save_model_creates_joblib_file(tmp_path):
    dataframe = pd.DataFrame(
        {
            "feature": range(10),
            "target": [0, 1] * 5,
        }
    )

    training_data = prepare_training_data(
        dataframe=dataframe,
        target_column="target",
        test_size=0.2,
    )

    pipeline = train_model(
        X_train=training_data.X_train,
        y_train=training_data.y_train,
        algorithm=Algorithm.RANDOM_FOREST,
    )

    model_path = save_model(
        pipeline=pipeline,
        output_dir=tmp_path,
    )

    assert model_path.endswith(".joblib")
    assert Path(model_path).exists()