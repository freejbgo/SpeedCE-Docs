"""Download and normalize public domain seed lists."""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

import aiohttp


TRANCO_TOP_URL = "https://tranco-list.eu/download/{list_id}/1000000"


async def fetch_tranco_top(
    list_id: str,
    *,
    limit: int = 10_000,
    session: aiohttp.ClientSession | None = None,
) -> list[dict[str, Any]]:
    """
    Fetch Tranco top list. Get a recent list_id from https://tranco-list.eu/
    Example list_id: 'L5VX9' (changes daily).
    """
    url = TRANCO_TOP_URL.format(list_id=list_id)
    owns = session is None
    if owns:
        session = aiohttp.ClientSession()
    try:
        async with session.get(url) as resp:
            resp.raise_for_status()
            text = await resp.text()
    finally:
        if owns and session is not None:
            await session.close()

    rows: list[dict[str, Any]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        domain = line.strip()
        if not domain:
            continue
        rows.append(
            {
                "domain": domain,
                "tranco_rank": i,
                "source": f"tranco:{list_id}",
            }
        )
        if len(rows) >= limit:
            break
    return rows


def filter_domains(
    rows: list[dict[str, Any]],
    *,
    include_tlds: list[str] | None = None,
    exclude_tlds: list[str] | None = None,
    exclude_vendors: list[str] | None = None,
    cdn_map: dict[str, list[str]] | None = None,
) -> list[dict[str, Any]]:
    """Pre-filter seeds before probing. cdn_map maps domain -> known vendors from prior runs."""
    include_tlds = [t.lower().lstrip(".") for t in (include_tlds or [])]
    exclude_tlds = [t.lower().lstrip(".") for t in (exclude_tlds or [])]
    exclude_vendors = set(exclude_vendors or [])
    cdn_map = cdn_map or {}

    out: list[dict[str, Any]] = []
    for row in rows:
        domain = row["domain"].lower()
        if include_tlds and not any(domain.endswith(f".{t}") or domain == t for t in include_tlds):
            continue
        if exclude_tlds and any(domain.endswith(f".{t}") or domain == t for t in exclude_tlds):
            continue
        if exclude_vendors:
            vendors = set(cdn_map.get(domain, []))
            if vendors & exclude_vendors:
                continue
        out.append(row)
    return out


def save_seed_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["domain", "tranco_rank", "source"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "domain": row["domain"],
                    "tranco_rank": row.get("tranco_rank") or "",
                    "source": row.get("source") or "",
                }
            )
