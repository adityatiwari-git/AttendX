# AttendX

AttendX is an attendance-management project repository.

The repository is currently being prepared for its application implementation. Project code and features will be added here as development continues.


## 🤖 Scheduled Project Maintenance

This repository has its own GitHub Actions maintenance workflow. It is **repository-local**, so it uses GitHub's built-in `GITHUB_TOKEN` instead of a personal access token or cross-repository secret.

### What the `.github/` folder is for

- `.github/workflows/daily-maintenance.yml` — runs the scheduled maintenance workflow.
- `.github/maintenance/schedule.json` — stores this repository's assigned dates and task names.
- `.github/maintenance/run_task.py` — contains the simple, predefined task logic.

The workflow runs at varied scheduled times defined in this repository's maintenance schedule and can also be started manually from the Actions tab.

Assigned October 2026 dates:
- 2026-10-06
- 2026-10-12
- 2026-10-17
- 2026-10-23
- 2026-10-28

The important rule is:

> **No meaningful change = no commit and no pull request.**

The workflow does not use Claude, OpenAI, or another external AI coding service. It only runs predefined repository-specific maintenance tasks, checks the result, and creates a draft PR when an actual change was made.

