# Git Workflow Cheat Sheet

Use this workflow when adding new features or fixes. It keeps the `main` branch stable and maintains a clean project history.

---

# Workflow Overview

| Phase | Action | Command |
|------|------|------|
| **1. Sync** | Update your local `main` branch | `git checkout main`<br>`git pull origin main` |
| **2. Branch** | Create a feature branch | `git checkout -b feature/your-feature-name` |
| **3. Build** | Stage and commit your changes | `git add .`<br>`git commit -m "your message"` |
| **4. Push** | Upload your branch to GitHub | `git push origin feature/your-feature-name` |
| **5. Merge** | Create and merge a Pull Request | Open PR on GitHub → Merge → `git pull` locally |

---

# Step-by-Step Guide

## 1. Prepare (Sync Your Local Repo)

Always start from the latest version of the project.

```bash
git checkout main
git pull origin main
```

---

## 2. Create a Branch

Work in a separate branch to isolate your changes.

Use clear prefixes:

- `feature/` – new features
- `fix/` – bug fixes
- `docs/` – documentation changes

Example:

```bash
git checkout -b feature/add-login-button
```

View all branches:

```bash
git branch
```

---

## 3. Work and Commit

Make your changes and commit them with a clear message.

```bash
git add .
git commit -m "feat: add login button to header"
```

Tip: Commit frequently with meaningful messages.

---

## 4. Push Your Branch

Upload your branch to GitHub for review.

```bash
git push origin feature/add-login-button
```

---

## 5. Open a Pull Request (PR)

1. Go to the repository on GitHub.
2. Click **"Compare & pull request"**.
3. Add a description of your changes.
4. Wait for review and merge.

---

## 6. Clean Up

After the PR is merged, update `main` and remove the old branch.

```bash
git checkout main
git pull origin main
git branch -d feature/add-login-button
```

---

# Quick Tips

### Check Status

If you're unsure what's happening:

```bash
git status
```

---

### Unstage a File

Remove a file from staging:

```bash
git reset HEAD <file>
```

---

### Sync While Working

If `main` changes while you're working on a feature branch:

```bash
git pull origin main
```

This keeps your branch up to date and reduces merge conflicts.

---

# Local Environment Setup

> Complete these steps **once** before running the project for the first time.

## 1. Create your `.env` file

The `.env` file holds secret credentials that Django needs at runtime (like the Google OAuth Client ID).
It is never committed to git — each teammate creates their own local copy.

Copy the template file to create your own `.env`:

```bash
# Run this from the root of the repo (the "main/" folder, where README.md lives).
# "cp" copies a file — it takes two arguments: source and destination.
# This copies the committed template (.env.example) into a new file (.env)
# that Django will actually read. You only need to run this once.
cp django/.env.example django/.env
```

Then open `django/.env` and replace the placeholder with the real Client ID.
Get the value from a teammate or from Google Cloud Console → APIs & Services → Credentials:

```
GOOGLE_OAUTH_CLIENT_ID=get_this_from_a_teammate_or_google_console
```

> **Note:** Never commit `.env` to git. It contains credentials and is gitignored on purpose.
> Committing it would expose your OAuth credentials publicly on GitHub.

## 2. Run the server

Once your `.env` is set up, start the Django development server:

```bash
# Navigate into the django project folder where manage.py lives
cd django

# Start the server on port 8000 (must match the port in Google Cloud Console)
python manage.py runserver 8000
```

Then open your browser at `http://localhost:8000` and Google OAuth should work.

---

# Admin User Setup

## 1. Edit django/.env and set

```bash
GOOGLE_ALLOWED_DOMAIN=bc.edu
ADMIN_PANEL_EMAILS=email1@bc.edu,email2@bc.edu
```
## 2. Go to the terminal and create a superuser

```bash
# Type
python manage.py createsuperuser
# Add the @bc.edu email that you added to the GOOGLE_ALLOWED_DOMAIN
# Enter password
```

## 3. Save changes and run the server

This Project is owned by Amaan, Billy, Dennis, Sebastian and Susan.
