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

