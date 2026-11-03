# AttendX security notes

- Django's password hashing and session authentication are used; passwords are never stored in profile fields.
- Public registration creates Student accounts only.
- Faculty and Administrator roles must be assigned by a trusted administrator.
- State-changing forms must use POST and CSRF tokens.
- Views must enforce role and object-level permissions on the server.
- Attendance records have a database uniqueness constraint per class session and student.
- Production must use a strong secret key, DEBUG=False, correct ALLOWED_HOSTS, HTTPS and secure cookie settings.
- Never commit .env files, production credentials, local databases or identifiable student information.
- The current V1 scaffold requires a complete security review and permission tests before production use.
