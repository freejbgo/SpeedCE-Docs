"""CLI entrypoint for the lead mining pipeline."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from .pipeline import load_seeds, run_pipeline, write_csv, write_json
from .seeds import fetch_tranco_top, save_seed_csv


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="CDN lead mining: probe domains and score prospects")
    sub = p.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch-tranco", help="Download Tranco top domains to CSV")
    fetch.add_argument("list_id", help="Tranco list ID from https://tranco-list.eu/")
    fetch.add_argument("-o", "--output", type=Path, default=Path("data/seeds/tranco.csv"))
    fetch.add_argument("-n", "--limit", type=int, default=5000)

    run = sub.add_parser("run", help="Probe seeds and export scored leads")
    run.add_argument("seeds", type=Path, help="Seed CSV or .txt (one domain per line)")
    run.add_argument("-o", "--output", type=Path, default=Path("data/leads/leads.csv"))
    run.add_argument("--json", type=Path, default=None, help="Optional JSON export path")
    run.add_argument("-c", "--concurrency", type=int, default=20)
    run.add_argument("--min-tier", choices=["hot", "warm", "cool", "low"], default="cool")
    run.add_argument("--user-agent", default=None)

    return p


TIER_ORDER = {"hot": 3, "warm": 2, "cool": 1, "low": 0}


def filter_by_tier(records, min_tier: str):
    threshold = TIER_ORDER[min_tier]
    return [r for r in records if TIER_ORDER.get(r.tier, 0) >= threshold]


async def async_main(args: argparse.Namespace) -> int:
    if args.command == "fetch-tranco":
        rows = await fetch_tranco_top(args.list_id, limit=args.limit)
        save_seed_csv(rows, args.output)
        print(f"Wrote {len(rows)} domains to {args.output}")
        return 0

    if args.command == "run":
        seeds = load_seeds(args.seeds)
        if not seeds:
            print(f"No seeds found in {args.seeds}")
            return 1
        kwargs = {}
        if args.user_agent:
            kwargs["user_agent"] = args.user_agent
        records = await run_pipeline(seeds, concurrency=args.concurrency, **kwargs)
        filtered = filter_by_tier(records, args.min_tier)
        write_csv(filtered, args.output)
        if args.json:
            write_json(filtered, args.json)
        print(
            f"Probed {len(records)} domains; exported {len(filtered)} "
            f"(min_tier={args.min_tier}) to {args.output}"
        )
        hot = sum(1 for r in filtered if r.tier == "hot")
        warm = sum(1 for r in filtered if r.tier == "warm")
        print(f"  hot={hot} warm={warm}")
        return 0

    return 1


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(asyncio.run(async_main(args)))


if __name__ == "__main__":
    main()
