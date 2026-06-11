"""Lightweight HTTP probing: TTFB, headers, asset hints — homepage only."""

from __future__ import annotations

import asyncio
import re
import time
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urljoin, urlparse

import aiohttp

from .cdn_fingerprints import CdnMatch, consolidate_matches, match_headers

DEFAULT_USER_AGENT = (
    "LeadMiner/0.1 (+https://example.com/bot; CDN prospect research; contact: ops@example.com)"
)

ASSET_HINT_RE = re.compile(
    r"""<(?:script|link|img|source)\b[^>]+(?:src|href)=["']([^"']+)["']""",
    re.I,
)


@dataclass
class ProbeResult:
    domain: str
    url: str
    ok: bool
    status: int | None = None
    ttfb_ms: float | None = None
    total_ms: float | None = None
    final_url: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    cdn_vendors: list[str] = field(default_factory=list)
    cdn_evidence: list[str] = field(default_factory=list)
    asset_count_hint: int = 0
    uses_https: bool = False
    error: str | None = None


async def probe_domain(
    domain: str,
    *,
    timeout: float = 10.0,
    user_agent: str = DEFAULT_USER_AGENT,
    session: aiohttp.ClientSession | None = None,
) -> ProbeResult:
    """Probe https then http homepage. Single GET, no deep crawl."""
    domain = domain.strip().lower().removeprefix("http://").removeprefix("https://").split("/")[0]
    owns_session = session is None
    if owns_session:
        connector = aiohttp.TCPConnector(ssl=False, limit=20)
        session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=timeout),
            headers={"User-Agent": user_agent},
        )

    result = ProbeResult(domain=domain, url=f"https://{domain}", ok=False)
    try:
        for scheme in ("https", "http"):
            url = f"{scheme}://{domain}/"
            started = time.perf_counter()
            try:
                async with session.get(  # type: ignore[union-attr]
                    url,
                    allow_redirects=True,
                    max_line_size=16384,
                    max_field_size=16384,
                ) as resp:
                    ttfb_ms = (time.perf_counter() - started) * 1000
                    body = await resp.text(errors="ignore")
                    total_ms = (time.perf_counter() - started) * 1000
                    headers = {k: v for k, v in resp.headers.items()}
                    http_matches = match_headers(headers)
                    vendors = consolidate_matches(http_matches)

                    result.ok = True
                    result.status = resp.status
                    result.ttfb_ms = round(ttfb_ms, 1)
                    result.total_ms = round(total_ms, 1)
                    result.final_url = str(resp.url)
                    result.headers = headers
                    result.cdn_vendors = vendors
                    result.cdn_evidence = [m.detail for m in http_matches]
                    result.uses_https = urlparse(str(resp.url)).scheme == "https"
                    result.asset_count_hint = _count_asset_hints(body, str(resp.url))
                    result.url = url
                    return result
            except (aiohttp.ClientError, asyncio.TimeoutError):
                continue
        result.error = "https and http both failed"
    finally:
        if owns_session and session is not None:
            await session.close()

    return result


def _count_asset_hints(html: str, base_url: str) -> int:
    count = 0
    for match in ASSET_HINT_RE.finditer(html[:200_000]):
        ref = match.group(1)
        if ref.startswith(("data:", "javascript:", "#")):
            continue
        absolute = urljoin(base_url, ref)
        host = urlparse(absolute).netloc
        if host and host not in (urlparse(base_url).netloc, ""):
            count += 1
    return count
