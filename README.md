# Flask REST API

A RESTful API built with Flask, featuring full CRUD operations for **Stores**, **Items**, and **Tags**. The project uses Flask-Smorest for API management and auto-generated Swagger UI documentation, Flask-SQLAlchemy for ORM-based database interaction, and Docker for containerized deployment.

---

## Features

- REST API with organized blueprints for Stores, Items, and Tags
- Auto-generated interactive API docs via Swagger UI (OpenAPI 3.0)
- SQLite database (default) with SQLAlchemy ORM
- Docker and Docker Compose support
- Environment variable configuration via `.flaskenv`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Flask |
| API Layer | Flask-Smorest |
| ORM | Flask-SQLAlchemy / SQLAlchemy |
| Serialization | Marshmallow (via Flask-Smorest schemas) |
| Database | SQLite (default) |
| Containerization | Docker / Docker Compose |
| Config | python-dotenv |

---

## Project Structure

```
flask-project-1/
├── app.py               # Application factory
├── db.py                # SQLAlchemy instance
├── schemas.py           # Marshmallow schemas
├── models/              # SQLAlchemy models
├── resources/
│   ├── item.py          # Item blueprint & routes
│   ├── store.py         # Store blueprint & routes
│   └── tag.py           # Tag blueprint & routes
├── instance/            # SQLite DB instance (auto-generated)
├── .flaskenv            # Flask environment variables
├── requirements.txt     # Python dependencies
├── dockerfile           # Docker image definition
└── docker-compose.yml   # Docker Compose configuration
```

---

## Getting Started

### Option 1 — Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/BrunoSecchiari/flask-project-1.git
cd flask-project-1
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
flask run
```

The API will be available at `http://localhost:5000`.

---

### Option 2 — Run with Docker

**1. Build and start the container**
```bash
docker-compose up --build
```

The API will be available at `http://localhost:5000`.

---

## API Documentation

Once the app is running, open your browser and navigate to:

```
http://localhost:5000/swagger-ui
```

This provides a full interactive Swagger UI where you can explore and test all endpoints.

---

## Environment Variables

The app reads configuration from `.flaskenv`. You can customize the following:

| Variable | Description | Default |
|---|---|---|
| `FLASK_APP` | Entry point for Flask | `app.py` |
| `FLASK_DEBUG` | Enable debug mode | `1` |
| `DATABASE_URL` | Database connection string | `sqlite:///data.db` |

---

## Requirements

```
flask
flask-smorest
flask-sqlalchemy
python-dotenv
sqlalchemy
```

Install all dependencies with:
```bash
pip install -r requirements.txt
```
