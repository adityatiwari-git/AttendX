# AttendX

**Smart Attendance Management System**

AttendX is a Django web application for academic attendance with Student, Faculty and Administrator roles.

## Technology

HTML5, CSS3, Bootstrap 5, JavaScript, Python, Django and PostgreSQL (SQLite for local development).

## Current implementation

- Django project configuration and modular apps: accounts, core, academics and attendance
- Custom user model with Student, Faculty and Administrator roles
- Django session authentication, login and logout
- Public student registration; privileged roles cannot self-assign
- Department, Course, Subject and Enrollment models
- Class sessions and attendance records with duplicate prevention
- Role-specific dashboards
- Initial faculty attendance session creation and editing
- Django Admin integration

## Run locally

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install and initialize:

```bash
python -m pip install -r requirements.txt
python manage.py makemigrations accounts academics attendance
python manage.py migrate
python manage.py createsuperuser
python manage.py check
python manage.py test
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Deploy on Koyeb

The repository includes a root `Procfile`, PostgreSQL-aware production settings and a step-by-step GitHub deployment guide:

**[docs/KOYEB_DEPLOYMENT.md](docs/KOYEB_DEPLOYMENT.md)**

Recommended zero-cost demo setup: Koyeb Free Web Service + Neon Free PostgreSQL. Free hosting is for previews and demos, not real institutional attendance data. Production mode requires `DJANGO_SECRET_KEY`, `DATABASE_URL`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`.

## Important status

This repository is an initial implementation and has not yet been independently verified as a complete production application. Generate and commit migrations, run Django checks and tests, review role permissions, and complete deployment smoke tests before presenting it as a working system. Faculty and administrator accounts must be provisioned by an administrator. Never commit secrets, local databases or real student records.

## Roadmap

- [x] Django foundation and modular apps
- [x] Authentication and role model
- [x] Academic and attendance data models
- [x] Role dashboards and initial faculty workflow
- [ ] Generated and committed migrations
- [ ] Automated tests and permission hardening
- [ ] Subject-wise student analytics and reports
- [ ] Admin workflows and UI polish
- [ ] Deployment validation and security review

## Documentation

See `docs/PROJECT_SCOPE.md`, `docs/DATABASE_DESIGN.md`, `docs/DEVELOPMENT_PLAN.md` and `docs/KOYEB_DEPLOYMENT.md`.
