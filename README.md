# Personal Voice AI Assistant (Django + Poetry)

This is your old Jarvis Lite project migrated from Flask to Django so you can practice Django workflows.

## Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Django
- Package manager: Poetry
- AI model provider: Groq (`llama3-8b-8192`)

## Project structure

```text
personal-voice-ai-assistant/
|-- backend/
|   |-- assistant/
|   |   |-- urls.py
|   |   `-- views.py
|   |-- config/
|   |   |-- settings.py
|   |   `-- urls.py
|   |-- manage.py
|   `-- .env.example
|-- frontend/
|   |-- index.html
|   |-- main.html
|   `-- script.js
`-- pyproject.toml
```

## Setup

1. Install dependencies:
   ```bash
   poetry install
   ```
2. Create env file:
   ```bash
   cp backend/.env.example backend/.env
   ```
3. Put your Groq key in `backend/.env`.
4. Run migrations:
   ```bash
   poetry run python backend/manage.py migrate
   ```
5. Start Django server:
   ```bash
   poetry run python backend/manage.py runserver
   ```
6. Open frontend (for example with VS Code Live Server) and use:
   - API endpoint: `http://127.0.0.1:8000/api/ask/`

## Notes for practice

- API route is now in `backend/assistant/views.py`.
- URL wiring is split across `backend/config/urls.py` and `backend/assistant/urls.py`.
- Settings and env handling are in `backend/config/settings.py`.
