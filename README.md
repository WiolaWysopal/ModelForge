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
* ✅ Health Check API
* ✅ Frontend ↔ Backend communication
* ✅ Backend unit tests

---

# 🛠 Tech Stack

## Backend

* Python
* FastAPI
* Pydantic Settings
* PostgreSQL

## Frontend

* React
* TypeScript
* Vite

## Infrastructure

* Docker
* Docker Compose

## Machine Learning*(planned)*

* scikit-learn
* MLflow
* NumPy
* pandas

## DevOps*(planned)*

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

---

# 🗺 Roadmap

## Project Foundation ✅

* FastAPI
* React
* PostgreSQL
* Docker
* Docker Compose
* Backend tests

## Planned

* SQLAlchemy
* Alembic
* Authentication
* Dataset Management
* Experiment Tracking
* Model Registry
* Model Training
* MLflow Integration
* Model Deployment
* Monitoring
* CI/CD
* Kubernetes

---

# 📌 Project Status

🚧 **Under active development** 

The project is being developed incrementally using feature branches and Pull Requests to simulate a professional software development workflow.
