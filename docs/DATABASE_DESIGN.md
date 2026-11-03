# AttendX V1 — Database Design (Initial Proposal)

This is the proposed relational model. Confirm the exact course/semester conventions with the intended institution before using real academic records.

## Identity
Use Django's authentication system. Prefer a custom User model configured before the first migration, with a role field (STUDENT, FACULTY, ADMIN) and institutional identifiers as appropriate. Do not store passwords in profile tables.

## Entities

### User
- id (primary key)
- username / email (unique login policy to decide)
- first_name, last_name
- role
- is_active, is_staff, is_superuser (Django-managed flags)

### Department
- id
- name
- code (unique)

### Course
- id
- department (FK Department)
- name
- code
- duration_years (optional)

### StudentProfile
- user (OneToOne FK User)
- enrollment_number (unique)
- course (FK Course)
- current_year / semester (bounded positive integers)
- admission_year

### FacultyProfile
- user (OneToOne FK User)
- employee_number (unique)
- department (FK Department)

### Subject
- id
- course (FK Course)
- code
- name
- semester
- faculty (FK FacultyProfile; consider a separate SubjectAssignment if multiple faculty teach a subject)

### Enrollment
- id
- student (FK StudentProfile)
- subject (FK Subject)
- academic_year
- unique constraint across student, subject, academic_year

### ClassSession
- id
- subject (FK Subject)
- faculty (FK FacultyProfile)
- session_date
- start_time (optional)
- topic (optional)
- status (SCHEDULED, COMPLETED, CANCELLED)
- created_at

### AttendanceRecord
- id
- session (FK ClassSession)
- student (FK StudentProfile)
- status (PRESENT, ABSENT)
- marked_by (FK FacultyProfile)
- marked_at
- updated_at
- unique constraint across session and student

## Relationships
- Department 1—many Course
- Course 1—many StudentProfile and Subject
- FacultyProfile 1—many Subject (initial single-faculty model)
- StudentProfile many—many Subject through Enrollment
- Subject 1—many ClassSession
- ClassSession 1—many AttendanceRecord
- StudentProfile 1—many AttendanceRecord

## Calculation
For one subject, let P = count of PRESENT attendance records and A = count of ABSENT attendance records for completed sessions. Percentage = 100 × P / (P + A). If P + A = 0, show Not available rather than dividing by zero.

## Important implementation notes
- Add database constraints for unique student/session attendance and enrollment.
- Use protected foreign keys where deleting a user or subject must not erase historical attendance.
- Decide whether student transfers, repeat subjects, and multiple faculty assignments need support before production use.
- SQLite is suitable for development and demonstration; evaluate PostgreSQL before multi-user production deployment.
