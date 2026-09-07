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

def test_preview_dataset(client, tmp_path, monkeypatch):
    upload_dir = tmp_path / "datasets"
    monkeypatch.setattr(datasets, "UPLOAD_DIR", upload_dir)

    csv_content = (
        b"name,age,city\n"
        b"Anna,25,Warsaw\n"
        b"Tom,30,London\n"
        b"Kate,28,Berlin\n"
        b"John,40,Paris\n"
        b"Maria,35,Rome\n"
        b"Alex,22,Madrid\n"
    )

    upload_response = client.post(
        "/datasets/upload",
        files={
            "file": (
                "preview.csv",
                BytesIO(csv_content),
                "text/csv",
            )
        },
    )

    assert upload_response.status_code == 200

    dataset_id = upload_response.json()["id"]

    preview_response = client.get(
        f"/datasets/{dataset_id}/preview"
    )

    assert preview_response.status_code == 200

    data = preview_response.json()

    assert data["dataset_id"] == dataset_id
    assert data["filename"] == "preview.csv"
    assert data["columns"] == ["name", "age", "city"]
    assert len(data["rows"]) == 5
    assert data["rows"][0] == {
        "name": "Anna",
        "age": 25,
        "city": "Warsaw",
    }

def test_preview_dataset_not_found(client):
    response = client.get("/datasets/999/preview")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Dataset not found."
    }

def test_preview_dataset_handles_missing_values(client, tmp_path, monkeypatch):
    upload_dir = tmp_path / "datasets"
    monkeypatch.setattr(datasets, "UPLOAD_DIR", upload_dir)

    csv_content = (
        b"name,age,city\n"
        b"Anna,25,Warsaw\n"
        b"Tom,,London\n"
    )

    upload_response = client.post(
        "/datasets/upload",
        files={
            "file": (
                "missing_preview.csv",
                BytesIO(csv_content),
                "text/csv",
            )
        },
    )

    assert upload_response.status_code == 200

    dataset_id = upload_response.json()["id"]

    preview_response = client.get(
        f"/datasets/{dataset_id}/preview"
    )

    assert preview_response.status_code == 200

    data = preview_response.json()

    assert data["rows"][1]["name"] == "Tom"
    assert data["rows"][1]["age"] is None
    assert data["rows"][1]["city"] == "London"