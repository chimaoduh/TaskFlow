# TaskFlow — Docker learning application

TaskFlow is a small but realistic task-management application for learning application packaging and multi-container deployment.

## Architecture in this starter

- **Frontend:** React + Vite
- **API:** Python + FastAPI
- **Database:** PostgreSQL via SQLAlchemy
- **Cache / broker dependency:** Redis (health check endpoint included)
- **Background worker:** Celery (demo task included)

This starter intentionally contains **no Dockerfile and no docker-compose.yml**. You will create those yourself during the lessons.

> Learning / security note: this is an educational MVP. It does not yet include user authentication, authorization, production-grade migrations, rate limiting, or hardened secrets management. Do not expose it publicly or use it for real customer data.

## Requirements

- Python 3.11 or newer
- Node.js 20 or newer
- PostgreSQL 15 or newer
- Redis 7 or newer
- Git Bash and VS Code

You can install PostgreSQL and Redis locally for the first run, or wait until the Docker lessons and run them as containers. The latter is a useful next exercise.

## Project structure

```text
TaskFlow/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── services/
│   │   ├── celery_app.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

## 1. Configure the backend

In Git Bash:

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and set `DATABASE_URL` to your local PostgreSQL credentials. Example:

```env
DATABASE_URL=postgresql+psycopg://taskflow:taskflow_dev_password@localhost:5432/taskflow
REDIS_URL=redis://localhost:6379/0
CORS_ORIGINS=http://localhost:5173
```

Create a PostgreSQL database named `taskflow` and a user named `taskflow`, or adjust the URL to match your local setup.

Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

On Windows Git Bash, if the activation command above does not work, try:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API documentation: http://localhost:8000/docs

## 2. Configure the frontend

Open a second Git Bash terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

The frontend expects the API at `http://localhost:8000`. You can override this by creating `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

## 3. Redis and Celery demo

Make sure Redis is running and that `REDIS_URL` is correct.

From the `backend` directory with the virtual environment active, start a worker:

```bash
celery -A app.celery_app.celery worker --loglevel=info --pool=solo
```

The `--pool=solo` option is useful for a first Windows/Git Bash learning setup. For Linux containers, we will use the normal worker pool.

Trigger the demo background task:

```bash
curl -X POST http://localhost:8000/api/tasks/demo-background-job
```

The task is sent to Celery through Redis. The worker logs the simulated notification.

## 4. Useful endpoints

- `GET /health` — API health
- `GET /health/dependencies` — checks PostgreSQL and Redis connectivity
- `GET /api/tasks` — list tasks
- `POST /api/tasks` — create a task
- `GET /api/tasks/{id}` — retrieve a task
- `PATCH /api/tasks/{id}` — update a task
- `DELETE /api/tasks/{id}` — delete a task
- `POST /api/tasks/demo-background-job` — enqueue a Celery demo task

Example task payload:

```json
{
  "title": "Prepare deployment checklist",
  "description": "Review environment variables and service dependencies.",
  "priority": "high",
  "status": "todo",
  "due_date": "2026-12-01T12:00:00"
}
```

## Docker learning path

Do not add all services at once. The recommended sequence is:

1. Run the API locally and understand `requirements.txt`.
2. Create a backend Dockerfile and build the API image.
3. Run PostgreSQL as a separate container and connect the API to it.
4. Add a named volume for PostgreSQL data.
5. Add Redis as a separate container.
6. Add the Celery worker.
7. Create a frontend Dockerfile.
8. Write `docker-compose.yml` to manage the services together.
9. Add Nginx only after the basic stack works.

Important networking rule: when the API runs inside Docker Compose, `localhost` means the API container itself. It should connect to PostgreSQL using the Compose service name (for example `db`) and Redis using `redis`, not `localhost`.

## Troubleshooting

- **API cannot connect to PostgreSQL:** confirm PostgreSQL is running, the database exists, and `DATABASE_URL` credentials are correct.
- **API cannot connect to Redis:** confirm Redis is running and `REDIS_URL` is correct.
- **Frontend cannot reach API:** confirm the API is running on port 8000 and check `VITE_API_URL`.
- **CORS error:** add the frontend origin to `CORS_ORIGINS`.
- **PowerShell vs Git Bash paths:** this guide uses Git Bash syntax.

## Next milestone

Once the app runs locally, we will containerize each component ourselves. The Dockerfiles and Compose file are deliberately left for you to create as part of the practical training.
