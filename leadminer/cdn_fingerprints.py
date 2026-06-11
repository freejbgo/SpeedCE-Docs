"""CDN vendor fingerprints from HTTP headers, DNS CNAMEs, and response patterns."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

# DNS CNAME suffixes → vendor label
CNAME_PATTERNS: list[tuple[str, str]] = [
    ("cloudflare.net", "Cloudflare"),
    ("cloudflare.com", "Cloudflare"),
    ("cloudfront.net", "AWS CloudFront"),
    ("akamaiedge.net", "Akamai"),
    ("akamaized.net", "Akamai"),
    ("edgesuite.net", "Akamai"),
    ("edgekey.net", "Akamai"),
    ("fastly.net", "Fastly"),
    ("fastlylb.net", "Fastly"),
    ("azureedge.net", "Azure CDN"),
    ("azurefd.net", "Azure Front Door"),
    ("googleusercontent.com", "Google Cloud CDN"),
    ("googlesyndication.com", "Google"),
    ("stackpathdns.com", "StackPath"),
    ("kxcdn.com", "KeyCDN"),
    ("b-cdn.net", "BunnyCDN"),
    ("cdn77.org", "CDN77"),
    ("incapdns.net", "Imperva"),
    ("hwcdn.net", "Highwinds"),
    ("llnwi.net", "Limelight"),
    ("lswcdn.net", "Leaseweb CDN"),
    ("alicdn.com", "Alibaba CDN"),
    ("kunlun", "Alibaba CDN"),
    ("qcloud.com", "Tencent CDN"),
    ("myqcloud.com", "Tencent CDN"),
    ("wsdvs.com", "Verizon EdgeCast"),
    ("edgecastcdn.net", "Verizon EdgeCast"),
    ("netlify.com", "Netlify"),
    ("vercel-dns.com", "Vercel"),
    ("github.io", "GitHub Pages"),
    ("shopifycdn.com", "Shopify"),
]

# (header_name_lower, regex_on_value, vendor) — checked case-insensitively on values
HEADER_PATTERNS: list[tuple[str, str, str]] = [
    ("server", r"cloudflare", "Cloudflare"),
    ("cf-ray", r".+", "Cloudflare"),
    ("cf-cache-status", r".+", "Cloudflare"),
    ("x-served-by", r"cache-", "Fastly"),
    ("x-cache", r"fastly", "Fastly"),
    ("x-fastly-request-id", r".+", "Fastly"),
    ("x-amz-cf-id", r".+", "AWS CloudFront"),
    ("x-amz-cf-pop", r".+", "AWS CloudFront"),
    ("x-cache", r"cloudfront", "AWS CloudFront"),
    ("x-akamai-", r".+", "Akamai"),
    ("x-ecdn", r".+", "Azure CDN"),
    ("x-azure-ref", r".+", "Azure CDN"),
    ("via", r"google", "Google Cloud CDN"),
    ("x-cdn", r".+", "Generic CDN"),
    ("x-cdn-pop", r".+", "Generic CDN"),
    ("x-edge-location", r".+", "Generic CDN"),
    ("x-bunny-", r".+", "BunnyCDN"),
    ("x-keycdn", r".+", "KeyCDN"),
]

# Competitors you may want to flag as "switchable" for overseas SME outreach
MAJOR_VENDORS = frozenset(
    {
        "Cloudflare",
        "AWS CloudFront",
        "Akamai",
        "Fastly",
        "Azure CDN",
        "Google Cloud CDN",
        "Alibaba CDN",
        "Tencent CDN",
    }
)


@dataclass(frozen=True)
class CdnMatch:
    vendor: str
    source: str  # "dns" | "http"
    detail: str


def match_cname(cname: str) -> str | None:
    lower = cname.lower().rstrip(".")
    for suffix, vendor in CNAME_PATTERNS:
        if lower.endswith(suffix) or suffix in lower:
            return vendor
    return None


def match_headers(headers: dict[str, str]) -> list[CdnMatch]:
    matches: list[CdnMatch] = []
    normalized = {k.lower(): v for k, v in headers.items()}
    for header, pattern, vendor in HEADER_PATTERNS:
        value = normalized.get(header)
        if value is None:
            # prefix match for headers like x-akamai-*
            if header.endswith("-"):
                for key, val in normalized.items():
                    if key.startswith(header) and re.search(pattern, val, re.I):
                        matches.append(CdnMatch(vendor, "http", f"{key}: {val[:120]}"))
            continue
        if re.search(pattern, value, re.I):
            matches.append(CdnMatch(vendor, "http", f"{header}: {value[:120]}"))
    return matches


def consolidate_matches(matches: Iterable[CdnMatch]) -> list[str]:
    seen: dict[str, CdnMatch] = {}
    for m in matches:
        if m.vendor not in seen:
            seen[m.vendor] = m
    return list(seen.keys())
