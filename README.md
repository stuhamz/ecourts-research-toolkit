# eCourts Research Toolkit

A provenance-first toolkit for collecting, preserving, screening and structuring **public Indian court records for cybercrime and digital-forensics research**.

This repository began as an eCourts cause-list scraper. Version 1.0 rebuilds it around a narrower and more defensible research problem:

> **How can publicly accessible court material be collected with provenance, screened for human-centric cybercrime, and transferred into a reproducible forensic research workflow without silently inventing facts or bypassing access controls?**

## Why this exists

Court orders and case-status material can contain unusually useful descriptions of:

- social-engineering pretexts
- impersonated identities
- victim actions
- financial flows
- phones, SIMs and CDRs
- account and device associations
- IP/login evidence
- forensic examinations
- prosecution allegations and defence challenges
- evidentiary gaps

But research use creates two problems.

First, a court record is a **source**, not automatically a verified factual narrative.

Second, scraping code can easily lose provenance: what URL was used, when it was accessed, which exact bytes were analysed, and whether the local text still corresponds to the original document.

This toolkit treats provenance as a first-class object.

## What v1.0 does

### 1. Ingest a manually downloaded court record

```bash
ecourts-research ingest-file order.pdf \
  --source-url "https://example.gov.in/order.pdf" \
  --title "Example court order" \
  --court "Example High Court" \
  --case-number "ABC/123/2026"
```

The toolkit stores the raw bytes locally and records:

- source URL
- access timestamp
- SHA-256 hash
- byte size
- content type
- local filename
- court/body
- case number
- research notes

### 2. Ingest a direct public URL

```bash
ecourts-research ingest-url "https://example.org/public-order"
```

This is for direct public pages or documents. It is **not** a CAPTCHA bypass mechanism.

### 3. Extract searchable text

Text extraction supports:

- PDF
- HTML
- plain text and common text-like formats

The original bytes remain preserved locally alongside `extracted.txt`.

### 4. Screen for cybercrime and social-engineering relevance

```bash
ecourts-research screen SRC-0123456789AB
```

The screening system is deliberately transparent and deterministic. It reports which terms matched across:

- social engineering
- manipulation mechanisms
- digital evidence
- cybercrime
- legal terminology

The score is a triage aid, **not a classifier of guilt, offence or legal outcome**.

### 5. Export candidates into the Social Engineering Incident Atlas workflow

```bash
ecourts-research export-atlas
```

This creates:

```text
output/atlas_candidates.csv
output/atlas_sources.csv
```

The candidate table uses Atlas-compatible fields and marks every new record `pending` for human screening.

### 6. Open current official eCourts services

```bash
ecourts-research portal case-status
ecourts-research portal cause-list
ecourts-research portal high-court
```

The toolkit opens the official service in the user's browser. CAPTCHA is completed manually by the user.

## Research workflow

```text
OFFICIAL / PUBLIC COURT SOURCE
            |
            v
     MANUAL SEARCH / RETRIEVAL
            |
            v
       SOURCE INGESTION
            |
            +--> raw source bytes
            +--> SHA-256
            +--> access timestamp
            +--> metadata.json
            +--> extracted.txt
            |
            v
     TRANSPARENT SCREENING
            |
            v
      HUMAN CASE REVIEW
            |
            v
   INCIDENT ATLAS CANDIDATE
```

## Installation

Python 3.11 or newer is recommended.

```bash
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick start

Open the current district-court case-status portal:

```bash
ecourts-research portal case-status
```

Download a relevant public order manually, then ingest it:

```bash
ecourts-research ingest-file "downloads/order.pdf" \
  --source-url "SOURCE_URL" \
  --court "COURT NAME"
```

List sources:

```bash
ecourts-research list-sources
```

Screen:

```bash
ecourts-research screen SOURCE_ID
```

Export for Atlas review:

```bash
ecourts-research export-atlas
```

## Local source layout

Raw source documents are **not committed to Git**.

```text
data/
  sources/
    SRC-<HASH>/
      metadata.json
      extracted.txt
      original-file.pdf
```

`data/sources/` is ignored except for `.gitkeep`.

## CNR validation

```bash
ecourts-research validate-cnr MHAU019999992015
```

Hyphens and spaces are removed before validation.

## Repository structure

```text
src/ecourts_research/
  atlas.py
  cli.py
  ecourts.py
  extract.py
  models.py
  provenance.py
  screen.py
  store.py

tests/
docs/
data/
output/
```

## Relationship to the Social Engineering Incident Atlas India

This repository is **collection and screening infrastructure**.

The Atlas is the curated research dataset.

Nothing is automatically inserted into the Atlas. The export step only generates `pending` candidates so the Atlas inclusion criteria, source-quality rules, coding protocol and attribution framework can still be applied manually.

## What this project deliberately does not do

- bypass CAPTCHA
- infer guilt
- treat bail-stage allegations as findings
- automatically decide whether a case belongs in the Atlas
- automatically assign attribution strength
- republish a corpus of source documents to GitHub
- claim that eCourts website information is itself legal evidence
- mass-crawl a public service without regard to access controls or site stability

## Testing

```bash
pytest
```

Lint:

```bash
ruff check .
```

## Responsible use

See [`docs/RESPONSIBLE_USE.md`](docs/RESPONSIBLE_USE.md).

## Project status

**v1.0.0 research rebuild**

The next engineering step is to add source-specific adapters only where they can be maintained and tested without weakening provenance or bypassing access controls.

## Author

**Hamzah**  
MSc Digital Forensics and Information Security  
National Forensic Sciences University, Delhi

Research interests: social engineering, digital forensics, OSINT, cybercrime reconstruction, electronic evidence and human-centric cybersecurity.
