# AttendX

**Smart Attendance Management for Educational Institutions**

AttendX is a web-based attendance management system designed to help educational institutions record, monitor, and review class attendance through role-specific workflows for students, faculty, and administrators.

> **Project status:** In development — V1 foundation and feature implementation are underway. This repository is the source of truth for the application code and documentation.

## Product goals

- Replace manual attendance registers and scattered spreadsheets with structured digital records.
- Give students a clear view of their overall and subject-wise attendance.
- Allow faculty to record and review attendance for assigned subjects.
- Give administrators a central way to manage academic entities and user access.
- Keep attendance calculations transparent and traceable to individual class records.

## V1 scope

### Student
- Secure sign-in and sign-out
- Student dashboard
- Overall and subject-wise attendance percentage
- Attendance history
- Profile details

### Faculty
- Faculty dashboard
- View assigned subjects and enrolled students
- Record attendance for a class/date
- Review attendance records
- Correct attendance records with appropriate authorization
- Basic attendance reports

### Administrator
- Manage student and faculty accounts
- Manage departments, courses, and subjects
- Assign faculty to subjects
- Review and manage attendance records
- Use Django Admin for privileged data management in the initial release

### Not included in V1
QR-code attendance, geofencing, facial recognition, parent accounts, native mobile apps, AI predictions, and institution-wide ERP integrations. These may be considered after the core attendance workflow is reliable.

## Technology

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Backend | Python, Django |
| Database | SQLite for development; deployment database to be assessed before launch |
| Version control | Git and GitHub |
| Deployment target | PythonAnywhere (planned) |

The project intentionally uses Django templates rather than React/Next.js so the implementation reinforces core frontend, backend, authentication, and database concepts.

## Application architecture

The Django project is organized by responsibility:

- `core` — public landing and shared pages
- `accounts` — authentication, user roles, and access control
- `students` — student-facing dashboard and profile
- `faculty` — faculty-facing workflows
- `attendance` — attendance records, calculations, and reports

Academic entities such as departments, courses, and subjects will be modeled in the domain app selected during implementation. Model ownership and relationships will be documented before migrations are finalized.

## Run locally

These instructions assume Python is installed.

1. Clone the repository:

   ```bash
   git clone https://github.com/adityatiwari-git/AttendX.git
   cd AttendX
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies once `requirements.txt` is present:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Apply migrations and start the development server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. Open http://127.0.0.1:8000/ in your browser.

> The application source and `requirements.txt` must be present before these run instructions can be completed. This README describes the intended V1 architecture; it does not claim that the application is already implemented or deployed.

## Development principles

- Use Django's built-in authentication and password hashing.
- Enforce role-based authorization on the server, not only in the UI.
- Protect state-changing forms with Django CSRF protection.
- Validate attendance inputs and prevent duplicate records for the same student, subject, and class session.
- Derive attendance percentages from recorded attendance data rather than storing manually editable percentages.
- Keep secrets and local databases out of version control.
- Add automated tests for permissions, attendance calculations, and attendance creation/editing.

## Roadmap

- [ ] Verify and restore the local Django project into this repository
- [ ] Establish Django project configuration and reusable templates
- [ ] Implement account model and role-based access
- [ ] Implement academic structure (department, course, subject, enrolment)
- [ ] Build student dashboard and attendance history
- [ ] Build faculty attendance workflow
- [ ] Build administrator workflows
- [ ] Add attendance reports and calculation tests
- [ ] Perform security, usability, and responsive checks
- [ ] Deploy a tested V1 instance
- [ ] Add deployment URL and application screenshots

## Documentation

Project requirements, database design, and deployment notes will be maintained in `docs/` as they are finalized.

## Author

**Aditya Tiwari**  
B.Tech Bioinformatics | Student Developer

## License

License to be selected before public reuse or distribution.
