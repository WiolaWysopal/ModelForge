# 🚀 ModelForge

> An open-source MLOps platform for training, tracking, deploying, and monitoring machine learning models.

ModelForge is a portfolio project that demonstrates how modern machine learning platforms are built using Python, FastAPI, React, Docker, PostgreSQL, and MLOps tools.

The long-term goal is to create an end-to-end platform for managing the complete machine learning lifecycle—from dataset management and experiment tracking to model deployment and monitoring.

---

# ✨ Current Features

* ✅ FastAPI backend
* ✅ React + TypeScript frontend
* ✅ Dockerized application
* ✅ Docker Compose environment
* ✅ PostgreSQL integration
* ✅ SQLAlchemy ORM
* ✅ Alembic database migrations
* ✅ Health Check API
* ✅ Frontend ↔ Backend communication
* ✅ Backend unit tests
* ✅ CSV dataset upload
* ✅ Dataset file type and size validation
* ✅ Dataset metadata persistence
* ✅ Automatic CSV analysis
* ✅ Row and column counting
* ✅ Missing value detection
* ✅ Dataset preview API

---

# 🛠 Tech Stack

## Backend

* Python
* FastAPI
* Pydantic Settings
* SQLAlchemy
* Alembic
* PostgreSQL

## Data Processing

* pandas
* NumPy

## Machine Learning *(planned)*

* scikit-learn
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
│   └── frontend/
│
├── infrastructure/
│   ├── kubernetes/
│   ├── mlflow/
│   └── monitoring/
│
├── data/
├── models/
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

---

## Available Services

| Service | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| Dataset Upload | POST /datasets/upload |
| Dataset Preview | GET /datasets/{dataset_id}/preview |

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

## PR 3 — Training Pipeline

* Target column selection
* Train/test split
* Data preprocessing
* Algorithm selection
* Model training
* Model persistence with joblib

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

---

# 📌 Project Status

🚧 **Under active development** 

The project is being developed incrementally using feature branches and Pull Requests to simulate a professional software development workflow.
