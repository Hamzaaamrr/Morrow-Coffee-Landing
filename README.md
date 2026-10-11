# Morrow Coffee website

Django serves the public landing page from `templates/menu/home.html`, with its styles, scripts, and photos in `static/coffee/`. Menu data is stored in SQLite and managed through the authenticated Django Admin.

## Local setup (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open the public site at <http://127.0.0.1:8000/> and menu management at <http://127.0.0.1:8000/admin/>. In development, Django creates and reuses a local key in the ignored `.django_secret_key` file. When `DJANGO_DEBUG=0`, set `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` in the environment; do not commit secrets to source control.

Menu items have a name, optional description, decimal price, and category. Categories retain their display order; items are listed alphabetically within each category. The public page handles empty categories and menu database errors.

SQLite is the local relational database (`db.sqlite3`). Before deployment, configure a production database and secret, set `DJANGO_DEBUG=0`, restrict `DJANGO_ALLOWED_HOSTS`, and run `python manage.py collectstatic`. Django's built-in Admin enforces authenticated user permissions for all management actions.
