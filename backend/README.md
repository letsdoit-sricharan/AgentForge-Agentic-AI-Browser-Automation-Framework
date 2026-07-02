# AgentForge Backend API

The backend engine and API services for AgentForge—a production-grade Agentic AI Automation Framework. Built on top of FastAPI, SQLAlchemy, and LangGraph.

## Architecture & Layout

The backend directory follows a clean, decoupled architecture:

```
backend/
├── app/
│   ├── api/          # FastAPI routers and endpoints
│   ├── core/         # Core config, logging, security, and orchestrator settings
│   ├── database/     # SQLAlchemy engine, session management, and migrations
│   ├── models/       # Database tables (SQLAlchemy models)
│   ├── schemas/      # Pydantic models for request/response serialization
│   ├── services/     # Business logic layers (agent controllers, executors)
│   ├── events/       # Event publishers and subscribers
│   ├── utils/        # Generic helper functions and middleware utilities
│   ├── __init__.py   # App package initialization
│   └── main.py       # FastAPI application entry point
├── tests/            # Test suite (pytest)
├── Dockerfile        # Containerization specification
├── pyproject.toml    # Dependency declarations and tooling configuration
└── requirements.txt  # Python dependency lock list
```

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL database

### Local Development Setup

1. **Clone the repository and navigate to the backend:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy `.env.example` to `.env` and fill in your configuration:
   ```bash
   cp .env.example .env
   ```

5. **Start the API Server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   The interactive OpenAPI docs will be available at `http://localhost:8000/docs`.
