"""Orchestrate seed ingestion → DNS → HTTP probe → score → CSV export."""

from __future__ import annotations

import asyncio
import csv
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import aiohttp

from .cdn_fingerprints import consolidate_matches
from .dns_lookup import resolve_a_records, resolve_cname_chain
from .http_probe import DEFAULT_USER_AGENT, probe_domain
from .scoring import LeadScore, score_lead


@dataclass
class LeadRecord:
    domain: str
    tranco_rank: int | None = None
    source: str = ""
    reachable: bool = False
    status: int | None = None
    ttfb_ms: float | None = None
    cdn_vendors: list[str] = field(default_factory=list)
    cdn_evidence: list[str] = field(default_factory=list)
    cname_chain: list[str] = field(default_factory=list)
    a_records: list[str] = field(default_factory=list)
    asset_count_hint: int = 0
    uses_https: bool = False
    final_url: str | None = None
    score: int = 0
    tier: str = "low"
    score_reasons: list[str] = field(default_factory=list)
    error: str | None = None


async def process_domain(
    domain: str,
    *,
    tranco_rank: int | None = None,
    source: str = "",
    semaphore: asyncio.Semaphore,
    session: aiohttp.ClientSession,
    dns_timeout: float = 5.0,
) -> LeadRecord:
    domain = domain.strip().lower()
    if not domain or domain.startswith("#"):
        return LeadRecord(domain=domain, error="empty")

    async with semaphore:
        record = LeadRecord(domain=domain, tranco_rank=tranco_rank, source=source)
        try:
            cname_chain, dns_matches = await resolve_cname_chain(domain, timeout=dns_timeout)
            a_records = await resolve_a_records(domain, timeout=dns_timeout)
            dns_vendors = consolidate_matches(dns_matches)

            probe = await probe_domain(domain, session=session)
            record.reachable = probe.ok
            record.status = probe.status
            record.ttfb_ms = probe.ttfb_ms
            record.cdn_vendors = list(dict.fromkeys(dns_vendors + probe.cdn_vendors))
            record.cdn_evidence = probe.cdn_evidence + [m.detail for m in dns_matches]
            record.cname_chain = cname_chain
            record.a_records = a_records
            record.asset_count_hint = probe.asset_count_hint
            record.uses_https = probe.uses_https
            record.final_url = probe.final_url
            record.error = probe.error

            lead_score: LeadScore = score_lead(probe, dns_vendors=dns_vendors, tranco_rank=tranco_rank)
            record.score = lead_score.score
            record.tier = lead_score.tier
            record.score_reasons = lead_score.reasons
        except Exception as exc:  # noqa: BLE001 — collect per-domain failures
            record.error = str(exc)
        return record


def load_seed_csv(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain = (row.get("domain") or row.get("host") or "").strip()
            if not domain:
                continue
            rank_raw = row.get("tranco_rank") or row.get("rank")
            tranco_rank = int(rank_raw) if rank_raw and str(rank_raw).isdigit() else None
            rows.append(
                {
                    "domain": domain,
                    "tranco_rank": tranco_rank,
                    "source": row.get("source") or path.name,
                }
            )
    return rows


def load_seed_lines(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        rows.append({"domain": line, "tranco_rank": None, "source": path.name})
    return rows


def load_seeds(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".csv":
        return load_seed_csv(path)
    return load_seed_lines(path)


async def run_pipeline(
    seeds: list[dict[str, Any]],
    *,
    concurrency: int = 20,
    user_agent: str = DEFAULT_USER_AGENT,
    dns_timeout: float = 5.0,
    http_timeout: float = 10.0,
) -> list[LeadRecord]:
    semaphore = asyncio.Semaphore(concurrency)
    connector = aiohttp.TCPConnector(ssl=False, limit=concurrency)
    timeout = aiohttp.ClientTimeout(total=http_timeout)
    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
        headers={"User-Agent": user_agent},
    ) as session:
        tasks = [
            process_domain(
                row["domain"],
                tranco_rank=row.get("tranco_rank"),
                source=row.get("source") or "",
                semaphore=semaphore,
                session=session,
                dns_timeout=dns_timeout,
            )
            for row in seeds
        ]
        return await asyncio.gather(*tasks)


def write_csv(records: list[LeadRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "domain",
        "tier",
        "score",
        "tranco_rank",
        "source",
        "reachable",
        "status",
        "ttfb_ms",
        "cdn_vendors",
        "uses_https",
        "asset_count_hint",
        "final_url",
        "cname_chain",
        "a_records",
        "score_reasons",
        "cdn_evidence",
        "error",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in sorted(records, key=lambda x: (-x.score, x.domain)):
            row = asdict(r)
            for key in ("cdn_vendors", "cname_chain", "a_records", "score_reasons", "cdn_evidence"):
                row[key] = "|".join(row[key]) if row[key] else ""
            writer.writerow({k: row.get(k) for k in fieldnames})


def write_json(records: list[LeadRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(r) for r in sorted(records, key=lambda x: (-x.score, x.domain))]
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
