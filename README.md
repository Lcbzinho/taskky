# taskky

Django project scaffolded for modeling exercise.

## Models
- Tag: name, slug
- Project: name, description, owner, created_at
- Task: title, description, status, due_date, project, assigned_to, tags, timestamps
- Comment: task, author, body, created_at

## Setup
```bash
# create venv (optional if using workspace venv)
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
```

## Migrations
Migrations generated via `python manage.py makemigrations tasks` and committed on branch `models`.
