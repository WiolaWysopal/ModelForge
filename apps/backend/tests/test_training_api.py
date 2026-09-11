from io import BytesIO

from app.api.routes import datasets, training


def upload_training_dataset(client, tmp_path, monkeypatch):
    upload_dir = tmp_path / "datasets"
    monkeypatch.setattr(datasets, "UPLOAD_DIR", upload_dir)

    csv_content = (
        b"age,city,target\n"
        b"20,Krakow,0\n"
        b"22,Warsaw,0\n"
        b"25,Krakow,0\n"
        b"28,Warsaw,0\n"
        b"30,Krakow,1\n"
        b"35,Warsaw,1\n"
        b"40,Krakow,1\n"
        b"45,Warsaw,1\n"
        b"50,Krakow,1\n"
        b"55,Warsaw,1\n"
    )

    response = client.post(
        "/datasets/upload",
        files={
            "file": (
                "training.csv",
                BytesIO(csv_content),
                "text/csv",
            )
        },
    )

    assert response.status_code == 200

    return response.json()["id"]


def test_train_dataset(client, tmp_path, monkeypatch):
    dataset_id = upload_training_dataset(
        client=client,
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
    )

    models_dir = tmp_path / "models"
    monkeypatch.setattr(
        training,
        "save_model",
        lambda pipeline: str(models_dir / "model.joblib"),
    )

    response = client.post(
        "/training",
        json={
            "dataset_id": dataset_id,
            "target_column": "target",
            "algorithm": "random_forest",
            "test_size": 0.2,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["dataset_id"] == dataset_id
    assert data["target_column"] == "target"
    assert data["algorithm"] == "random_forest"
    assert data["test_size"] == 0.2
    assert data["train_size"] == 8
    assert data["test_size_rows"] == 2
    assert data["model_path"].endswith("model.joblib")


def test_train_dataset_not_found(client):
    response = client.post(
        "/training",
        json={
            "dataset_id": 999,
            "target_column": "target",
            "algorithm": "random_forest",
            "test_size": 0.2,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Dataset not found."
    }


def test_train_dataset_rejects_missing_target_column(
    client,
    tmp_path,
    monkeypatch,
):
    dataset_id = upload_training_dataset(
        client=client,
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
    )

    response = client.post(
        "/training",
        json={
            "dataset_id": dataset_id,
            "target_column": "missing_target",
            "algorithm": "random_forest",
            "test_size": 0.2,
        },
    )

    assert response.status_code == 422
    assert "Target column" in response.json()["detail"]