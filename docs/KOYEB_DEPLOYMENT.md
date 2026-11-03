# Deploy AttendX on Koyeb (GitHub → Koyeb)

This guide targets a **$0 hobby/demo deployment**, not production use with real institutional attendance records.

## Recommended zero-cost architecture

- **Application:** Koyeb Free Web Service, deployed from the private or public GitHub repository.
- **Database:** Neon Free PostgreSQL, connected using `DATABASE_URL`.
- **Source of truth:** GitHub repository `adityatiwari-git/AttendX`, branch `main`.

Koyeb's free instance currently provides 512 MB RAM, 0.1 vCPU and 2 GB SSD. It is limited to one free web service per organization, has no persistent volumes, and sleeps after one hour without traffic. Koyeb states that free instances are intended for previews and hobby projects, not production applications. Its included free PostgreSQL database has only five active compute hours per month, so use an external database for this demo.

Neon's Free plan currently includes 100 CU-hours per project per month, 1 GB PostgreSQL storage per project, and 5 GB public network transfer. Compute suspends after five minutes of inactivity. Free-plan limits can change; check provider pricing before relying on them.

## Before deployment — required

1. Generate Django migrations locally and commit them to GitHub. Do not deploy before migration files are in the repository.
2. Run `python manage.py check` and `python manage.py test`.
3. Create a Neon project and copy its PostgreSQL connection string. Use the pooled connection string if Neon provides one for your setup.
4. Keep the database URL and Django secret private. Never commit them to GitHub.

Generate a secret key after installing the project dependencies:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Create the Koyeb service

1. Sign in at https://app.koyeb.com/.
2. Choose **Create Web Service** and select **GitHub**.
3. Install/authorize the Koyeb GitHub App for the `adityatiwari-git/AttendX` repository.
4. Select repository `adityatiwari-git/AttendX` and branch `main`.
5. Choose the **Buildpack** builder and the repository root as the work directory.
6. Keep the repository's root `Procfile`. It runs migrations, collects static files, and starts Gunicorn.
7. Select the **Free** instance type and one supported free region (Frankfurt or Washington, D.C.).
8. Enable automatic deployment from the `main` branch if the option is shown.

Koyeb's official Django instructions use GitHub + Buildpack and require the public host to be included in `DJANGO_ALLOWED_HOSTS`. The Procfile in this repository defines the web process.

## Environment variables

Add these in Koyeb's service configuration before deploying:

| Name | Value |
|---|---|
| `DJANGO_SECRET_KEY` | The newly generated secret key |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `{{ KOYEB_PUBLIC_DOMAIN }}` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://{{ KOYEB_PUBLIC_DOMAIN }}` |
| `DATABASE_URL` | Neon PostgreSQL connection URL |

Do not add quotes around these values. Keep `DATABASE_URL` private. Production settings intentionally refuse to start without a persistent database URL.

## First launch and smoke test

Once Koyeb reports a successful deployment:

1. Open the Koyeb service console/shell and run `python manage.py createsuperuser`.
2. Visit `https://YOUR-SERVICE.koyeb.app/admin/`.
3. Create fictional demo departments, courses, subjects, faculty accounts and student enrollments.
4. Test student registration/login, faculty attendance marking, student dashboards and role restrictions.
5. Push a harmless README change to `main` and confirm Koyeb starts a new deployment automatically.

## Limitations and safety

- The Koyeb Free instance sleeps after one hour of inactivity; the first request after sleep can be delayed.
- The Neon free database sleeps after five minutes of inactivity and has monthly compute/network quotas.
- Free services can change their limits or terms. Monitor both provider dashboards.
- Do not use the free demo for real student records or sensitive institutional data. Before real use, arrange paid/persistent hosting, backups, access controls, audit logs, privacy review and institutional approval.
- A successful deploy is not proof that the application is production-ready. Complete migrations, automated tests and permission/security review first.
