# 🚀 ModelForge

> An open-source MLOps platform for training, tracking, deploying, and monitoring machine learning models.

ModelForge is a portfolio project that demonstrates how modern machine learning platforms are built using Python, FastAPI, React, Docker, PostgreSQL, and MLOps tools.

The long-term goal is to create an end-to-end platform for managing the complete machine learning lifecycle—from dataset management and model training to experiment tracking, deployment, and monitoring.

---

# ✨ Current Features

* ✅ FastAPI backend
* ✅ React + TypeScript frontend
* ✅ Dockerized application
* ✅ Docker Compose environment
* ✅ PostgreSQL integration
* ✅ SQLAlchemy ORM
* ✅ Alembic database migrations
* ✅ Automatic database migrations on backend startup
* ✅ Health Check API
* ✅ Frontend ↔ Backend communication
* ✅ Backend unit and API tests
* ✅ CSV dataset upload
* ✅ Dataset file type and size validation
* ✅ Dataset metadata persistence
* ✅ Automatic CSV analysis
* ✅ Row and column counting
* ✅ Missing value detection
* ✅ Dataset preview API
* ✅ Target column selection
* ✅ Train/test dataset splitting
* ✅ Numeric and categorical feature preprocessing
* ✅ Missing value imputation
* ✅ Numeric feature scaling
* ✅ Categorical feature encoding
* ✅ Logistic Regression training
* ✅ Random Forest training
* ✅ Trained model persistence with joblib
* ✅ Model Training API

---

# 🛠 Tech Stack

## Backend

* Python
* FastAPI
* Pydantic
* Pydantic Settings
* SQLAlchemy
* Alembic
* PostgreSQL

## Data Processing

* pandas
* NumPy

## Machine Learning

* scikit-learn
* joblib

### Planned

* MLflow

## Frontend

* React
* TypeScript
* Vite

## Infrastructure

* Docker
* Docker Compose

## DevOps *(planned)*

* GitHub Actions
* Kubernetes
* Prometheus
* Grafana

---

# 📂 Project Structure

```text
ModelForge/
│
├── apps/
│   ├── backend/
│   │   ├── alembic/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── core/
│   │   │   ├── models/
│   │   │   ├── schemas/
│   │   │   └── services/
│   │   ├── data/
│   │   │   ├── datasets/
│   │   │   └── models/
│   │   └── tests/
│   │
│   └── frontend/
│
├── infrastructure/
│   ├── kubernetes/
│   ├── mlflow/
│   └── monitoring/
│
├── docker-compose.yml
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

* Docker Desktop
* Docker Compose
* Git

---

## Run the application

Clone the repository:

```bash
git clone https://github.com/WiolaWysopal/ModelForge.git
cd ModelForge
```

Start the entire platform:

```bash
docker compose up --build
```

Database migrations are applied automatically before the backend starts.

---

## Available Services

| Service | URL / Endpoint |
|----------|----------------|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Health Check | GET /health |
| Dataset Upload | POST /datasets/upload |
| Dataset Preview | GET /datasets/{dataset_id}/preview |
| Model Training | POST /training |

---

# 🗺 Roadmap

## PR 1 — Project Foundation ✅

* FastAPI backend
* React + TypeScript frontend
* PostgreSQL
* Docker
* Docker Compose
* Health Check API
* Frontend ↔ Backend communication
* Backend tests

## PR 2 — Dataset Management ✅

* SQLAlchemy ORM
* Alembic migrations
* CSV dataset upload
* File type validation
* File size validation
* Dataset metadata persistence
* Row and column counting
* Missing value detection
* Dataset preview

## PR 3 — Training Pipeline ✅

* Target column selection
* Train/test split
* Numeric and categorical data preprocessing
* Missing value imputation
* Numeric feature scaling
* Categorical feature encoding
* Algorithm selection
* Logistic Regression
* Random Forest
* Model training
* Model persistence with joblib
* Training API endpoint
* Training pipeline tests
* Automatic database migrations on Docker startup

## PR 4 — Experiment Tracking

* Experiment history
* Accuracy
* Precision
* Recall
* F1-score
* Training duration
* Model parameters
* Experiment comparison

## PR 5 — Model Registry & Inference

* Model versioning
* Active model selection
* Prediction API
* Prediction testing from the UI

## PR 6 — MLflow Integration

* MLflow experiment tracking
* Metrics and parameters logging
* Model artifacts
* MLflow UI

## Future

* Authentication
* CI/CD with GitHub Actions
* Kubernetes
* Prometheus
* Grafana
* Model monitoring

---

# 🔌 API

## Upload Dataset

```http
POST /datasets/upload
```

Uploads a CSV dataset, validates the file, stores it, and calculates dataset metadata including:

* number of rows
* number of columns
* number of missing values

## Preview Dataset

```http
GET /datasets/{dataset_id}/preview
```

Returns dataset metadata, column names, and the first five rows of the uploaded dataset.

## Train Model

```http
POST /training
```

Trains a machine learning model using a previously uploaded dataset.

Example request:

```json
{
  "dataset_id": 1,
  "target_column": "category",
  "algorithm": "random_forest",
  "test_size": 0.2
}
```

The training pipeline:

1. loads the selected dataset,
2. separates features from the target column,
3. creates the train/test split,
4. preprocesses numeric and categorical features,
5. trains the selected algorithm,
6. persists the fitted pipeline as a `.joblib` model artifact.

Currently supported algorithms:

* `logistic_regression`
* `random_forest`

Example response:

```json
{
  "dataset_id": 1,
  "target_column": "category",
  "algorithm": "random_forest",
  "test_size": 0.2,
  "train_size": 80,
  "test_size_rows": 20,
  "model_path": "data/models/<model-id>.joblib"
}
```

---

# 📌 Project Status

🚧 **Under active development**

The project is being developed incrementally using feature branches and Pull Requests to simulate a professional software development workflow.

PR 1 established the project foundation, PR 2 introduced dataset management, and PR 3 adds the first end-to-end machine learning training pipeline. The next development stage focuses on experiment tracking and model evaluation.