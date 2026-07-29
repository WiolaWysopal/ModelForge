# ModelForge

ModelForge is an MLOps platform for training, tracking, deploying, and monitoring machine learning models.

The project is designed to demonstrate practical software engineering, machine learning, and DevOps skills by providing an end-to-end workflow for managing ML experiments.

## Tech Stack

### Backend

- FastAPI
- Python
- PostgreSQL

### Frontend

- React
- TypeScript

### Machine Learning

- scikit-learn
- NumPy
- pandas

### DevOps

- Docker
- Kubernetes
- GitHub Actions

## Getting Started

### Backend

```bash
cd apps/backend

python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

python -m uvicorn app.main:app --reload
```

## Planned Features

- Dataset management
- Model training
- Experiment tracking
- Model registry
- Prediction API
- MLflow integration
- Monitoring with Prometheus and Grafana

## Project Structure

```bash
ModelForge/
│
├── apps/
│ ├── backend/
│ └── frontend/
│
├── infrastructure/
│ ├── kubernetes/
│ ├── mlflow/
│ └── monitoring/
│
├── data/
├── models/
│
└── README.md
```


## Status

🚧 Project under development.