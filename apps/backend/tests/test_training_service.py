import pandas as pd
import pytest

from app.services.training import prepare_training_data


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