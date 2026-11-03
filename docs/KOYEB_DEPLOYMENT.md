# Deploy AttendX on Koyeb

AttendX can be deployed from the GitHub repository using Koyeb's GitHub integration.

## Important architecture notes

- Use a managed PostgreSQL database and set its connection string as `DATABASE_URL`.
- Do not use SQLite for a hosted multi-user deployment. Koyeb's free web instance has ephemeral local storage and cannot attach a persistent volume.
- Koyeb's free PostgreSQL database is limited to 5 hours of active compute per month. For a continuously available demo database, use an external provider such as Neon and review its current free-plan limits.
- Keep all credentials in Koyeb environment variables. Never commit secrets or production database URLs.

## Koyeb service configuration

1. Sign in to Koyeb and choose **Create Web Service**.
2. Choose **GitHub** and connect the GitHub account if prompted.
3. Select `adityatiwari-git/AttendX`, branch `main`.
4. Select the **Buildpack** builder.
5. Use the repository root as the working directory.
6. The root `Procfile` supplies the web command. If Koyeb asks for a run command, use the same command from that file.
7. Add the environment variables below before deploying.

## Required environment variables

| Variable | Value |
|---|---|
| `DJANGO_SECRET_KEY` | A newly generated, private random secret |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `{{ KOYEB_PUBLIC_DOMAIN }}` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://{{ KOYEB_PUBLIC_DOMAIN }}` |
| `DATABASE_URL` | PostgreSQL connection URL from the database provider |

Do not put quotation marks around the values in the Koyeb dashboard. Keep the database URL private.

## First deployment and administrator setup

After the first deployment succeeds, open a Koyeb Shell/console for the running service and create the administrator with:

```bash
python manage.py createsuperuser
```

Then test `/admin/`, registration, login, dashboards and the attendance workflow using fictional demo data only.

## Before presenting to real users

Run and commit Django migrations from the development environment, complete the test suite, review role permissions, configure database backups, and perform a security/privacy review. A successful deployment alone does not mean the application is production-ready.
