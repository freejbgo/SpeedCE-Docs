"""Passive DNS reconnaissance for CDN CNAME chains."""

from __future__ import annotations

import asyncio
from typing import Any

from .cdn_fingerprints import CdnMatch, match_cname

try:
    import dns.asyncresolver
    import dns.exception
except ImportError:  # pragma: no cover
    dns = None  # type: ignore[assignment]


async def resolve_cname_chain(hostname: str, timeout: float = 5.0) -> tuple[list[str], list[CdnMatch]]:
    """Return CNAME chain and any CDN matches found in the chain."""
    if dns is None:
        raise RuntimeError("dnspython is required: pip install dnspython")

    resolver: Any = dns.asyncresolver.Resolver()
    resolver.lifetime = timeout
    chain: list[str] = []
    matches: list[CdnMatch] = []
    current = hostname.rstrip(".")

    for _ in range(10):
        try:
            answers = await resolver.resolve(current, "CNAME")
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.DNSException):
            break
        cname = str(answers[0].target).rstrip(".")
        chain.append(cname)
        vendor = match_cname(cname)
        if vendor:
            matches.append(CdnMatch(vendor, "dns", cname))
        current = cname

    return chain, matches


async def resolve_a_records(hostname: str, timeout: float = 5.0) -> list[str]:
    if dns is None:
        raise RuntimeError("dnspython is required: pip install dnspython")

    resolver: Any = dns.asyncresolver.Resolver()
    resolver.lifetime = timeout
    try:
        answers = await resolver.resolve(hostname.rstrip("."), "A")
        return [str(r) for r in answers]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.DNSException):
        return []
