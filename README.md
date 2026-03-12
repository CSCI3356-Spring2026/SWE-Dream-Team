# Git Workflow Cheat Sheet

Follow this process to add new features or fixes. This ensures a clean project history and prevents breaking the `main` branch.

---

## The Workflow Cycle

| Phase | Action | Command |
| :--- | :--- | :--- |
| **1. Sync** | Update your local main | `git checkout main` && `git pull origin main` |
| **2. Branch** | Create a new workspace | `git checkout -b feature/your-feature-name` |
| **3. Build** | Stage and save changes | `git add .` && `git commit -m "your message"` |
| **4. Ship** | Upload to GitHub | `git push origin feature/your-feature-name` |
| **5. Merge** | Finalize the feature | Create PR on GitHub → Merge → `git pull` on local |

---

## Step-by-Step Guide

### 1. Prepare
Always start from the latest version of the code.
```bash
git checkout main
git pull origin main
