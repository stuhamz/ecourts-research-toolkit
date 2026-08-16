from __future__ import annotations

import json
from pathlib import Path

import click

from .atlas import export_atlas_candidates, export_atlas_sources
from .ecourts import is_valid_cnr, normalize_cnr, open_portal, portal_url
from .screen import screen_text
from .store import SourceStore


def _store(data_dir: str) -> SourceStore:
    return SourceStore(data_dir)


@click.group()
@click.option(
    "--data-dir",
    default="data",
    show_default=True,
    envvar="ECOURTS_RESEARCH_HOME",
    help="Local research data directory. Raw source material is not intended for Git.",
)
@click.pass_context
def cli(ctx: click.Context, data_dir: str) -> None:
    """Collect, preserve, screen and structure public Indian court material."""
    ctx.ensure_object(dict)
    ctx.obj["data_dir"] = data_dir


@cli.command("ingest-file")
@click.argument("path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--source-url", default=None)
@click.option("--title", default=None)
@click.option("--source-type", default="court_record", show_default=True)
@click.option("--authority", default=None, help="Publisher or authority.")
@click.option("--court", default=None, help="Court or body.")
@click.option("--case-number", default=None)
@click.option("--notes", default=None)
@click.pass_context
def ingest_file(
    ctx: click.Context,
    path: Path,
    source_url: str | None,
    title: str | None,
    source_type: str,
    authority: str | None,
    court: str | None,
    case_number: str | None,
    notes: str | None,
) -> None:
    """Ingest a manually downloaded court file with provenance metadata."""
    metadata = _store(ctx.obj["data_dir"]).ingest_file(
        path,
        source_url=source_url,
        title=title,
        source_type=source_type,
        publisher_or_authority=authority,
        court_or_body=court,
        case_number=case_number,
        notes=notes,
    )
    click.echo(json.dumps(metadata.to_dict(), indent=2, ensure_ascii=False))


@cli.command("ingest-url")
@click.argument("url")
@click.option("--title", default=None)
@click.option("--source-type", default="court_record", show_default=True)
@click.option("--authority", default=None)
@click.option("--court", default=None)
@click.option("--case-number", default=None)
@click.option("--notes", default=None)
@click.pass_context
def ingest_url(
    ctx: click.Context,
    url: str,
    title: str | None,
    source_type: str,
    authority: str | None,
    court: str | None,
    case_number: str | None,
    notes: str | None,
) -> None:
    """Retrieve a direct public URL and preserve the returned bytes and metadata."""
    metadata = _store(ctx.obj["data_dir"]).ingest_url(
        url,
        title=title,
        source_type=source_type,
        publisher_or_authority=authority,
        court_or_body=court,
        case_number=case_number,
        notes=notes,
    )
    click.echo(json.dumps(metadata.to_dict(), indent=2, ensure_ascii=False))


@cli.command("list-sources")
@click.pass_context
def list_sources(ctx: click.Context) -> None:
    """List locally ingested sources."""
    for source in _store(ctx.obj["data_dir"]).list_sources():
        click.echo(f"{source.source_id}\t{source.title}\t{source.source_url or ''}")


@cli.command("show")
@click.argument("source_id")
@click.pass_context
def show(ctx: click.Context, source_id: str) -> None:
    """Show provenance metadata for one source."""
    metadata = _store(ctx.obj["data_dir"]).get_metadata(source_id)
    click.echo(json.dumps(metadata.to_dict(), indent=2, ensure_ascii=False))


@cli.command("screen")
@click.argument("source_id")
@click.pass_context
def screen(ctx: click.Context, source_id: str) -> None:
    """Run transparent rule-based cybercrime/social-engineering screening."""
    store = _store(ctx.obj["data_dir"])
    result = screen_text(source_id, store.get_text(source_id))
    click.echo(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


@cli.command("screen-all")
@click.pass_context
def screen_all(ctx: click.Context) -> None:
    """Screen all locally ingested sources."""
    store = _store(ctx.obj["data_dir"])
    results = [
        screen_text(source.source_id, store.get_text(source.source_id)).to_dict()
        for source in store.list_sources()
    ]
    click.echo(json.dumps(results, indent=2, ensure_ascii=False))


@cli.command("export-atlas")
@click.option(
    "--candidates",
    default="output/atlas_candidates.csv",
    show_default=True,
    type=click.Path(path_type=Path),
)
@click.option(
    "--sources",
    "sources_path",
    default="output/atlas_sources.csv",
    show_default=True,
    type=click.Path(path_type=Path),
)
@click.option("--reviewer", default="Hamzah", show_default=True)
@click.pass_context
def export_atlas(
    ctx: click.Context,
    candidates: Path,
    sources_path: Path,
    reviewer: str,
) -> None:
    """Export Atlas-compatible candidate and source tables for human review."""
    store = _store(ctx.obj["data_dir"])
    c = export_atlas_candidates(store, candidates, reviewer=reviewer)
    s = export_atlas_sources(store, sources_path)
    click.echo(f"Candidates: {c}")
    click.echo(f"Sources:    {s}")


@cli.command("validate-cnr")
@click.argument("cnr")
def validate_cnr(cnr: str) -> None:
    """Normalize and validate a 16-character eCourts CNR identifier."""
    normalized = normalize_cnr(cnr)
    click.echo(f"normalized={normalized}")
    if not is_valid_cnr(normalized):
        raise click.ClickException("CNR must contain 16 alphanumeric characters.")
    click.echo("valid=true")


@cli.command("portal")
@click.argument(
    "name",
    type=click.Choice(["district", "case-status", "cause-list", "high-court"]),
)
@click.option("--open/--no-open", "open_browser", default=True, show_default=True)
def portal(name: str, open_browser: bool) -> None:
    """Open an official eCourts portal for manual search/CAPTCHA completion."""
    url = portal_url(name)
    if open_browser:
        open_portal(name)
    click.echo(url)


if __name__ == "__main__":
    cli()
