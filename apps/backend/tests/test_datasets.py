from io import BytesIO

from app.api.routes import datasets


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
    assert data["row_count"] == 0
    assert data["column_count"] == 0
    assert data["missing_values_count"] == 0
    assert "id" in data
    assert "file_path" in data
    assert "created_at" in data

    saved_file = tmp_path / data["file_path"]

    assert saved_file.exists()
    assert saved_file.read_bytes() == csv_content