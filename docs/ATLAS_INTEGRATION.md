# Social Engineering Incident Atlas Integration

## Intended flow

1. Search public court services manually.
2. Download or retrieve a candidate source.
3. Ingest it into the local source store.
4. Run transparent screening.
5. Export Atlas candidate and source tables.
6. Review the candidate under the Atlas inclusion/exclusion criteria.
7. Only then assign an Atlas case ID and perform full incident coding.

## Export files

### `output/atlas_candidates.csv`

Uses the Atlas screening-log field structure.

Every row is exported with:

`decision = pending`

This is deliberate.

### `output/atlas_sources.csv`

Uses the Atlas source-registry structure but leaves case-level fields blank until an incident has passed screening.

## Provenance transfer

The source export stores the SHA-256 digest in `notes`.

The Atlas may later add a dedicated source-hash field if this proves useful across a larger corpus.
