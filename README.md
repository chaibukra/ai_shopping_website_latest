# 🛒 AI-Driven E-Commerce Platform & Predictive Analytics

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

A high-performance, asynchronous e-commerce backend and administrative platform. Designed utilizing the **Controller-Service-Repository structural pattern**, this system integrates an LLM-powered shopping assistant via the **Gemini API** and hosts an embedded machine learning inference pipeline for forecasting customer expenses.

---

## 🏗️ Architectural Pattern & Highlights

The application strictly adheres to the **Layered (Multi-Tier) Architecture** to ensure clean separation of concerns, testability, and maintainability:
* **Controllers:** Handle HTTP request routing, input validation, and Role-Based Access Control (RBAC).
* **Services:** Encapsulate core business logic, orchestration, and external AI/ML inferences.
* **Repositories:** Manage data persistence and abstract state logic for both relational database (MySQL) and caching (Redis) layers.

---

## ⚙️ Core Technical Highlights

* **Asynchronous Processing:** Built entirely with **FastAPI** utilizing Python's `async/await` syntax for non-blocking I/O and high throughput.
* **Multi-Layer Performance Caching:** Implemented a dedicated cache repository using **Redis** to offload frequent data lookups, minimizing database read operations.
* **ML Production Deployment:** Deployed a supervised polynomial regression pipeline trained in **Scikit-Learn**, serialized via `joblib`, and served securely under admin-restricted endpoints.
* **Automated CI/CD Pipeline:** Integrated with **GitHub Actions** (`build_and_push_to_dockerhub.yml`) to automatically test, build multi-stage Docker images, and push deliverables straight to **Docker Hub**.

---

## 📂 Project Structure

├── .github/workflows/
│   └── build_and_push_to_dockerhub.yml  # Automated CI/CD workflow
├── config/
│   └── config.py                        # App configuration & env parsing
├── controller/                          # API HTTP Endpoints (Routing & RBAC)
│   ├── auth_controller.py
│   ├── predict_controller.py            # ML Model serving endpoints
│   └── ... (item, order, user, favorite controllers)
├── exceptions/
│   └── security_exceptions.py            # Global custom app exceptions
├── machine_learning_model/              # ML Pipeline artifacts
│   ├── CustomerShopping.ipynb           # Training notebook & data analytics
│   ├── final_customer_model.joblib      # Serialized regression model
│   └── polynomial_converter.joblib      # Feature transformers
├── model/                               # Pydantic schemas & data contract entities
│   ├── auth_response.py
│   └── ... (item, order, user request/response models)
├── redisClient/
│   └── redis_client.py                  # Redis connection pool management
├── repository/                          # Data Access Layer (SQLAlchemy & Caching)
│   ├── database.py                      # SQLAlchemy async engine configuration
│   ├── cache_repository.py              # Redis abstraction layer
│   └── ... (user, order, item repositories)
├── resources/db-migrations/
│   └── init.sql                         # Database schema & seed initialization
├── service/                             # Core Business Logic Layer
│   ├── predict_service.py               # Serialized model inference orchestration
│   └── ... (auth, user, order, item business logic)
├── ui/                                  # Frontend Client Layer
│   └── ... (Streamlit application pages & custom web UI components)
├── main.py                              # FastAPI Application entry point
├── Dockerfile.fastapi                   # Multi-stage build for the backend
├── Dockerfile.streamlit                 # Multi-stage build for the frontend UI
└── docker-compose.yml                   # Local multi-container orchestration ecosystem

---

## 🚀 Getting Started

### Prerequisites
Ensure you have the following orchestration tools installed locally:
* Docker Desktop / Docker Compose

### 1. Environment Setup
Clone this repository to your local workspace and navigate into the root directory:

git clone [https://github.com/chaibukra/ai_shopping_website_latest.git](https://github.com/chaibukra/ai_shopping_website_latest.git)
cd ai_shopping_website_latest

Create a .env file in the root directory and define your runtime configurations. Ensure you supply a valid Gemini API Key:

DATABASE_URL=mysql+pymysql://root:password@db:3306/shopping_db
REDIS_HOST=redis
REDIS_PORT=6379
SECRET_KEY=your_super_secret_jwt_signing_key
BASE_URL=http://web:8000
GEMINI_API_KEY=your_actual_gemini_api_key

### 2. Local Infrastructure Orchestration
Spin up the entire decoupled ecosystem (FastAPI Server, Streamlit UI, MySQL DB, and Redis) using Docker Compose:

docker-compose up -d --build

The system components will initialize and be accessible at:
* Interactive Backend API Documentation (Swagger): http://localhost:8000/docs
* Streamlit E-Commerce Customer & Admin Portal: http://localhost:8501

---

## 🧠 Machine Learning Engine & Inference Pipeline

The administrative predictive module acts as a production-level deployment of an analytical model:
1. Pipeline Serialization: The model pipeline utilizes engineered features and polynomial conversions (polynomial_converter.joblib & customer_scaler.joblib) created inside the Jupyter environment.
2. Production Serving: When an authorized administrator calls the predict_user_expenses_for_tech_items endpoint, the predict_controller forwards the task to the predict_service. The service loads the pipeline via joblib, processes user transactional parameters, and yields instant calculated inferences in USD.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or open a Pull Request.
