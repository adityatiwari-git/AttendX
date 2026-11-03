# AttendX

**Smart Attendance Management System**

AttendX is a Django web application for academic attendance with Student, Faculty and Administrator roles.

## Technology
HTML5, CSS3, Bootstrap 5, JavaScript, Python, Django and SQLite.

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
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python manage.py makemigrations accounts academics attendance
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Open http://127.0.0.1:8000/.

## Important
This is an initial implementation scaffold, not a verified production release. It still requires local installation, migrations, Django checks, automated tests, security review and deployment validation. Faculty and administrator accounts must be provisioned by an administrator. Never commit secrets, local databases or real student records.

## Roadmap
- [x] Django foundation and modular apps
- [x] Authentication and role model
- [x] Academic and attendance data models
- [x] Role dashboards and initial faculty workflow
- [ ] Automated tests and permission hardening
- [ ] Subject-wise student analytics and reports
- [ ] Admin workflows and UI polish
- [ ] Production configuration and deployment

## Documentation
See docs/PROJECT_SCOPE.md, docs/DATABASE_DESIGN.md and docs/DEVELOPMENT_PLAN.md.
