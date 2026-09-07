from io import BytesIO

from app.api.routes import datasets

from app.core.config import settings

def test_upload_dataset(client, tmp_path, monkeypatch):
    upload_dir = tmp_path / "datasets"
    monkeypatch.setattr(datasets, "UPLOAD_DIR", upload_dir)

    csv_content = b"age,height,weight\n25,165,60\n30,172,75\n"

    response = client.post(
        "/datasets/upload",
        files={
            "file": (
                "test_dataset.csv",
                BytesIO(csv_content),
                "text/csv",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test_dataset.csv"
    assert data["row_count"] == 2
    assert data["column_count"] == 3
    assert data["missing_values_count"] == 0
    assert "id" in data
    assert "file_path" in data
    assert "created_at" in data 

    saved_file = tmp_path / data["file_path"]

    assert saved_file.exists()
    assert saved_file.read_bytes() == csv_content

def test_upload_rejects_non_csv_file(client):
    response = client.post(
        "/datasets/upload",
        files={
            "file": (
                "notes.txt",
                BytesIO(b"not a csv file"),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Only CSV files are allowed."
    }

def test_upload_rejects_file_larger_than_limit(client, monkeypatch):
    monkeypatch.setattr(settings, "max_upload_size_mb", 1)

    oversized_content = b"a" * (1024 * 1024 + 1)

    response = client.post(
        "/datasets/upload",
        files={
            "file": (
                "large.csv",
                BytesIO(oversized_content),
                "text/csv",
            )
        },
    )

    assert response.status_code == 413
    assert response.json() == {
        "detail": "File is too large. Maximum size is 1 MB."
    }

def test_upload_dataset_detects_missing_values(client, tmp_path, monkeypatch):
    upload_dir = tmp_path / "datasets"
    monkeypatch.setattr(datasets, "UPLOAD_DIR", upload_dir)

    csv_content = b"name,age,city\nAnna,25,Warsaw\nTom,,London\nKate,30,\n"

    response = client.post(
        "/datasets/upload",
        files={
            "file": (
                "missing_values.csv",
                BytesIO(csv_content),
                "text/csv",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["row_count"] == 3
    assert data["column_count"] == 3
    assert data["missing_values_count"] == 2