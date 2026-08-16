# Replacement Push Guide

This rebuild is intended to replace the old prototype cleanly.

The old repository committed a virtual environment, so its reachable Git history remains unnecessarily large even if `venv/` is merely deleted.

## Recommended approach

### 1. Back up the current repository

```powershell
git clone https://github.com/stuhamz/ecourts-scraper.git ecourts-scraper-old
```

### 2. Extract this rebuild into a new directory

For example:

```text
ecourts-research-toolkit-v1.0.0/
```

### 3. Initialise a clean repository

Inside the rebuilt folder:

```powershell
git init
git branch -M main
git remote add origin https://github.com/stuhamz/ecourts-scraper.git
git add .
git commit -m "Rebuild as provenance-first eCourts research toolkit"
```

### 4. Inspect before replacing the remote

```powershell
git status
git ls-files
```

Confirm that `venv/`, `.venv/`, `__pycache__/`, raw `data/sources/`, and generated `output/` files are absent.

### 5. Replace the old prototype branch

Because this intentionally replaces an early prototype history:

```powershell
git push --force-with-lease origin main
```

If `--force-with-lease` rejects because this new local repository has never fetched the remote, run:

```powershell
git fetch origin main
git push --force-with-lease origin main
```

Do not use plain `--force` unless you understand the difference.

## After the push

Recommended repository name:

`ecourts-research-toolkit`

GitHub redirects the old repository URL after a rename.

Recommended description:

> Provenance-first collection and screening of public Indian court records for cybercrime and digital-forensics research.

Recommended topics:

- digital-forensics
- cybercrime
- ecourts
- legal-research
- social-engineering
- electronic-evidence
- osint
- dfir
- india
- research-toolkit
