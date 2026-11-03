# AttendX

<p align="center">
  <strong>A role-based attendance management system for academic institutions.</strong>
  <br />
  Built with Django, Python, and a responsive Bootstrap interface.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" />
  <img alt="Django" src="https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white" />
  <img alt="Bootstrap" src="https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white" />
  <img alt="Database" src="https://img.shields.io/badge/Database-PostgreSQL%20%7C%20SQLite-4169E1?logo=postgresql&logoColor=white" />
</p>

## Overview

AttendX is a web-based attendance management project designed to organise academic attendance in one place. It provides separate experiences for students, faculty members, and administrators, with Django handling authentication, application logic, and data management.

The project is being developed incrementally, with an emphasis on clear role separation, connected academic records, reliable attendance history, and a maintainable application structure.

## Technology stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Backend | Python, Django |
| Database | SQLite for local development; PostgreSQL for hosted deployment |
| Static files | WhiteNoise |
| Application server | Gunicorn |
| Hosting | Render |
| Database hosting | Neon PostgreSQL (planned configuration) |
| Version control & delivery | Git, GitHub (deployment connected to the repository) |

## Current features

- **Role-based accounts:** Student, Faculty, and Administrator roles using a custom Django user model.
- **Authentication:** Django session-based login and logout.
- **Student registration:** Public registration creates student accounts only; privileged roles cannot be self-assigned.
- **College-wide academic structure:** Departments, programmes/courses, academic batches, student profiles, semester-specific subjects, enrollments, and weekly timetable entries.
- **Multi-department faculty assignments:** A faculty member can be assigned to subjects across programmes and departments.\n- **Semester history:** Student dashboards present semester-wise attendance archives and current-semester subject enrolments.\n- **Faculty workspace:** Assigned subjects, cross-programme teaching schedule, class sessions, student registers, and attendance concerns.
- **Class sessions:** Faculty can create attendance sessions for subjects.
- **Attendance records:** Present, Absent, and Late statuses, with a database constraint preventing duplicate records for the same student and session.
- **Role-specific dashboards:** Separate dashboard views based on account role.
- **Attendance management:** Faculty attendance entry and editing through a formset.
- **Django Admin:** Administrative access to the underlying application models.

## Project structure

```text
AttendX/
├── accounts/       # Custom user model and authentication
├── academics/      # Departments, courses, subjects, enrollments
├── attendance/     # Class sessions and attendance records
├── core/           # Shared pages and dashboard routing
├── templates/      # Django HTML templates
├── static/         # CSS and frontend assets
├── attendx/        # Django project settings and URL configuration
├── manage.py
├── requirements.txt
├── Procfile
└── README.md
```

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/adityatiwari-git/AttendX.git
cd AttendX
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Create database migrations and initialise the database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create an administrator account and start the server

```bash
python manage.py createsuperuser
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser. The Django admin is available at **http://127.0.0.1:8000/admin/**.

> SQLite is used for local development; the hosted setup uses PostgreSQL.

## Development status

AttendX is an actively developing project. The repository now includes the college-wide academic data model, multi-faculty subject assignments, semester archive views, and timetable data structures alongside the core attendance workflow. It should not yet be treated as a production-ready institutional system.

Before real-world use, the project still needs generated and committed migrations, broader automated test coverage, a complete permissions review, deployment verification, and a security/privacy review. Use fictional data for demonstrations.

## Roadmap

- [x] Django project foundation and modular apps
- [x] Custom user model and role-based authentication
- [x] Academic structure and enrollment models
- [x] Class session and attendance record models
- [x] Initial role dashboards and faculty attendance workflow
- [ ] Verify generated database migrations and hosted schema update
- [ ] Expand automated tests and harden role/object permissions
- [ ] Add subject-wise attendance analytics and report exports
- [ ] Improve administrative workflows and interface polish
- [ ] Complete hosted deployment and security validation

## Contributing

Contributions and suggestions are welcome. For substantial changes, create a focused branch and include relevant tests.

---

<p align="center">
  <sub>AttendX · Academic Attendance Management</sub>
</p>
