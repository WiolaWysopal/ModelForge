import pytest
from pydantic import ValidationError

from app.schemas.training import Algorithm, TrainingRequest


def test_training_request_with_valid_data():
    request = TrainingRequest(
        dataset_id=1,
        target_column="species",
        algorithm=Algorithm.RANDOM_FOREST,
        test_size=0.2,
    )

    assert request.dataset_id == 1
    assert request.target_column == "species"
    assert request.algorithm == Algorithm.RANDOM_FOREST
    assert request.test_size == 0.2


def test_training_request_uses_default_test_size():
    request = TrainingRequest(
        dataset_id=1,
        target_column="species",
        algorithm=Algorithm.LOGISTIC_REGRESSION,
    )

    assert request.test_size == 0.2


@pytest.mark.parametrize("test_size", [0, 1, -0.1, 1.1])
def test_training_request_rejects_invalid_test_size(test_size):
    with pytest.raises(ValidationError):
        TrainingRequest(
            dataset_id=1,
            target_column="species",
            algorithm=Algorithm.RANDOM_FOREST,
            test_size=test_size,
        )


def test_training_request_rejects_invalid_algorithm():
    with pytest.raises(ValidationError):
        TrainingRequest(
            dataset_id=1,
            target_column="species",
            algorithm="svm",
        )