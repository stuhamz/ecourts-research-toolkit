# Screening Method

## Purpose

The screening score helps answer one narrow question:

> Which retrieved documents deserve human review first for social-engineering and digital-forensics research?

It does not predict guilt or legal relevance.

## Groups

The current vocabulary has five weighted groups:

- social engineering: weight 4 per unique matched term
- manipulation: weight 3
- digital evidence: weight 2
- cybercrime: weight 2
- legal: weight 1

The complete vocabulary is in `src/ecourts_research/screen.py`.

## Category suggestion

A preliminary attack-category hint is based on simple keyword overlap.

It must be treated as a suggestion only.

## Why no LLM coding in v1

The first engineering goal is reproducibility.

A deterministic screen is easier to inspect, test and falsify than an opaque automatic case-coding system.
