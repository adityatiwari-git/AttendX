# AttendX V1 — Project Scope

## Problem
Colleges may rely on paper registers or disconnected spreadsheets to capture class attendance. Students can find it difficult to track attendance across subjects, while faculty spend time recording and consolidating records.

## Proposed solution
AttendX is a Django-based web application that provides structured attendance records and role-specific views for students, faculty, and administrators.

## V1 users and permissions

| Role | Main capabilities |
|---|---|
| Student | View own overall and subject attendance, history, and profile |
| Faculty | View assigned subjects and rosters; record and review attendance for assigned classes |
| Administrator | Manage users and academic structure; oversee attendance records |

Permissions must be enforced server-side. Hiding a button is not an authorization control.

## V1 features
1. Authentication and role-based access
2. Departments, courses, subjects, faculty assignments, and student enrolments
3. Faculty attendance entry for a subject and class session
4. Student attendance summary and history
5. Basic reports and administrative management
6. Responsive Bootstrap interface

## Explicitly out of scope
QR attendance, GPS/geofencing, face recognition, parent portals, AI predictions, native mobile apps, and third-party ERP integrations.

## Attendance definition
A class session belongs to one subject and has a date/time and responsible faculty member. Each enrolled student should have at most one attendance record per session. Attendance percentage is calculated from session records according to an explicitly documented denominator. Initial V1 rule: Present / (Present + Absent) × 100. Cancelled sessions and excused absences are excluded from the denominator if those statuses are introduced.

## Acceptance criteria
- Students cannot view another student's private attendance history.
- Faculty can only record or amend attendance for subjects assigned to them.
- Duplicate attendance for one student/session is prevented at the database level.
- Percentages are calculated from stored records and tested.
- All state-changing forms use POST and CSRF protection.
- Core pages work on mobile and desktop.
- The project starts from documented setup instructions and passes Django system checks and tests.
