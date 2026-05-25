# TaskFlow

> A minimalist task manager with multi-project support, HTMX-powered UI, and user authentication.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, Django 5.2 |
| Auth | django-allauth |
| Frontend | Bootstrap 5, HTMX, Alpine.js |
| Database | PostgreSQL 16 (Docker) |
| Container | Docker + docker-compose |
| Lint | Ruff |
| Deploy | Railway / Render / Fly.io |

## Features

- 🗂 Multiple TODO lists (projects) visible on a single page
- ✅ Create, edit, and delete tasks without page reload (HTMX)
- 🔼🔽 Reorder tasks with ↑ / ↓ buttons
- ✏️ Task controls appear on hover (Alpine.js)
- 🔐 Registration and login via django-allauth
- 🐳 Fully containerized environment

## Getting Started (Docker)

```bash
# 1. Clone the repository
git clone https://github.com/Senndin/taskflow.git
cd taskflow

# 2. Create the environment file
cp .env.example .env
# Edit .env if needed

# 3. Start the containers (PostgreSQL + Django)
docker-compose up -d

# 4. Apply database migrations
docker-compose exec web python manage.py migrate

# 5. Create a superuser (optional)
docker-compose exec web python manage.py createsuperuser

# 6. Open in browser
open http://localhost:8000
```

### Stop the project

```bash
docker-compose down        # stop and remove containers (data is preserved)
docker-compose down -v     # stop and also remove database data
```

## Getting Started (Local, SQLite — no Docker)

```bash
# 1. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up .env
cp .env.example .env
# In .env, replace DATABASE_URL with:
# DATABASE_URL=sqlite:///db.sqlite3

# 4. Apply migrations and run the server
python manage.py migrate
python manage.py runserver
```

## Project Structure

```
taskflow/
├── config/
│   ├── settings/
│   │   ├── base.py        # shared settings
│   │   ├── local.py       # development
│   │   └── production.py  # production
│   └── urls.py
├── apps/
│   ├── core/              # base.html, 404, 500
│   ├── projects/          # Project model, CRUD
│   └── tasks/             # Task model, CRUD, move up/down
├── static/css/
├── templates/
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Environment Variables

| Variable | Description | Example |
|----------|------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode | `True` / `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `127.0.0.1,localhost` |
| `DATABASE_URL` | Database connection URL | `postgresql://user:pass@db:5432/taskflow` |

## Useful Commands

```bash
# Open a shell inside the container
docker-compose exec web bash

# Django interactive shell
docker-compose exec web python manage.py shell

# Run Ruff linter
docker-compose exec web ruff check .

# Create and apply migrations after model changes
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## Deployment

The project is ready to deploy on Railway, Render, or Fly.io.

1. Set `DEBUG=False` and configure `DATABASE_URL` in the platform's environment variables
2. Set `SECRET_KEY` to a random, secure string
3. After deployment, run `python manage.py migrate && python manage.py collectstatic`

---

*Developed as a test project assignment.*
