# Architecture

## Design principle

The toolkit separates four jobs that the original prototype mixed together:

1. **retrieval**
2. **preservation**
3. **screening**
4. **research coding**

Only the first three belong here. Final incident coding belongs in the Social Engineering Incident Atlas.

## Source store

Every ingested object receives a deterministic source ID based on the first 12 hexadecimal characters of its SHA-256 digest.

The full digest remains in `metadata.json`.

If identical bytes are ingested twice, they receive the same source ID. This helps identify exact duplicate documents.

## Why raw sources stay local

Public availability does not mean every court document should be republished in a Git repository.

Keeping source bytes local:

- reduces privacy amplification
- avoids needlessly duplicating third-party material
- keeps the repository small
- separates software from research corpus
- allows researchers to retain provenance without redistributing source files

## Screening

The screening module uses explicit weighted term lists.

It is designed for prioritisation, not automated factual coding.

Every match is inspectable.

## Atlas boundary

`export-atlas` creates pending candidate/source rows.

It does not:
- include the case
- assign evidentiary strength
- normalise legal provisions
- determine attribution
