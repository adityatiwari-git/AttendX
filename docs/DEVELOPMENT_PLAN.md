# AttendX V1 — Development Plan

## Milestone 0: Recover and verify
- Inspect the developer's local VS Code project folder.
- Preserve a backup before making changes.
- Confirm Git root, branch, remote URL, ignored files, and local commits.
- Restore existing Django files if present; do not recreate over them blindly.

## Milestone 1: Foundation
- Django project configuration
- core, accounts, students, faculty, and attendance apps
- Templates and static files
- Bootstrap base layout and landing page
- .gitignore, requirements.txt, and setup documentation

## Milestone 2: Identity and permissions
- Custom user model (before first migration)
- Student and faculty profiles
- Login/logout
- Role-based route and object-level permissions
- Authentication and authorization tests

## Milestone 3: Academic structure
- Departments, courses, subjects
- Faculty subject assignments
- Student enrolments
- Django Admin configuration

## Milestone 4: Attendance workflow
- Create class sessions
- Record present/absent status per enrolled student
- Prevent duplicate records
- Allow authorized correction with audit metadata
- Validate dates, enrolments, and faculty assignments

## Milestone 5: Student experience
- Student dashboard
- Overall and subject-wise percentages
- Attendance history
- Profile page

## Milestone 6: Faculty experience
- Faculty dashboard
- Subject roster
- Attendance marking and review
- Basic reports

## Milestone 7: Quality and deployment
- Automated tests and manage.py check
- Responsive/accessibility review
- Production settings, secret management, HTTPS and allowed hosts
- Deployment and smoke test
- Add screenshots and live URL to README

## Git workflow
Commit each tested milestone with a meaningful message. Never commit .env, virtual environments, local database files containing personal data, or secrets. Keep the default branch deployable; use feature branches for larger changes.
