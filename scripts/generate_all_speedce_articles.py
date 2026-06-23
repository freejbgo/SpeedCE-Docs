#!/usr/bin/env python3
"""Regenerate all 100 SpeedCE promotional articles (batch 1 + batch 2)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_speedce_articles import ARTICLES as BATCH1
from generate_speedce_articles_batch2 import ARTICLES_BATCH2
from speedce_articles_common import write_articles, write_readme

if __name__ == "__main__":
    write_articles(BATCH1)
    write_articles(ARTICLES_BATCH2)
    write_readme(BATCH1 + ARTICLES_BATCH2)
    print(f"Regenerated {len(BATCH1) + len(ARTICLES_BATCH2)} articles in docs/articles/")
