# AttendX deployment checklist

Deployment is not complete until the application has been installed and smoke-tested on the hosting provider.

## Before deployment
1. Run the full test suite and Django system checks.
2. Set a unique DJANGO_SECRET_KEY in the host environment.
3. Set DJANGO_DEBUG=False.
4. Set DJANGO_ALLOWED_HOSTS to the exact host name.
5. Configure HTTPS and secure cookies at the host.
6. Run migrations on the production database.
7. Collect static files.
8. Create a private administrator account.
9. Use fictional demo data only for public demonstrations.

## PythonAnywhere outline
1. Create a PythonAnywhere web app using the supported Python version.
2. Clone the GitHub repository into the account.
3. Create a virtual environment and install requirements.txt.
4. Configure the WSGI file to point to attendx.wsgi.application.
5. Set environment variables in the WSGI configuration or host settings.
6. Configure static files to serve STATIC_ROOT after collectstatic.
7. Run migrations and create a superuser.
8. Reload the web app and test login, role restrictions and attendance workflows.

## Important
SQLite is used for development. Before multi-user institutional use, evaluate a managed PostgreSQL database, backups, restore procedures, audit requirements, privacy rules and institutional approval. Do not upload real student data to a public demo.
