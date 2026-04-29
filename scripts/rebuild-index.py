#!/usr/bin/env python3
# maps · cassette.help · MIT
"""
rebuild-index.py — Rebuild readings/index.json and feed.xml from actual files.

Scans readings/daily/{date}/*.website.md and reconstructs the manifest.
Safe to run any time — does not touch git, does not post anything.

Usage:
    python3 scripts/rebuild-index.py
    python3 scripts/rebuild-index.py --dry-run
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

SITE_ROOT = Path(__file__).parent.parent
READINGS_DAILY = SITE_ROOT / "readings" / "daily"
INDEX_PATH = SITE_ROOT / "readings" / "index.json"
FEED_PATH = SITE_ROOT / "feed.xml"
SITE_URL = "https://cassette.help"


def extract_card_name(md_text: str, reading_type: str) -> str:
    if reading_type == "iching-integration":
        m = re.search(r"##\s+hexagram\s+\d+:\s+(.+)", md_text, re.I)
        if m:
            return m.group(1).strip()
    if reading_type == "three-card":
        bold = re.findall(r"\*\*([^*]+)\*\*", md_text)[:3]
        if len(bold) >= 3:
            return " · ".join(bold)
    m = re.search(r"\*\*([^*]+)\*\*", md_text)
    return m.group(1).strip() if m else ""


def rebuild_manifest() -> dict:
    dates: dict = {}
    reading_types = ["single-card", "three-card", "iching-integration"]

    if not READINGS_DAILY.exists():
        print(f"ERROR: {READINGS_DAILY} not found", file=sys.stderr)
        sys.exit(1)

    for date_dir in sorted(READINGS_DAILY.iterdir(), reverse=True):
        if not date_dir.is_dir():
            continue
        date_str = date_dir.name
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            continue
        for rtype in reading_types:
            f = date_dir / f"{rtype}.website.md"
            if not f.exists():
                continue
            name = extract_card_name(f.read_text(), rtype)
            if date_str not in dates:
                dates[date_str] = {}
            dates[date_str][rtype] = name

    return {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dates": dates,
    }


def rebuild_feed(manifest: dict) -> str:
    dates_sorted = sorted(manifest["dates"].keys(), reverse=True)[:20]
    first_updated = (dates_sorted[0] + "T12:00:00Z") if dates_sorted else datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        f'  <title>NO SLEEP CASSETTE — daily oracle</title>',
        f'  <link href="{SITE_URL}/"/>',
        f'  <link rel="self" type="application/atom+xml" href="{SITE_URL}/feed.xml"/>',
        f'  <id>{SITE_URL}/</id>',
        f'  <updated>{first_updated}</updated>',
        f'  <author><name>maps</name><email>bitch@cassette.help</email></author>',
        f'  <subtitle>daily tarot · I Ching · astrology by maps</subtitle>',
    ]
    for date_str in dates_sorted:
        d = manifest["dates"][date_str]
        parts = [v for k, v in sorted(d.items()) if v]
        title = date_str + (" — " + " · ".join(parts) if parts else "")
        summary = " / ".join(parts) if parts else "readings for " + date_str
        lines += [
            "  <entry>",
            f"    <id>{SITE_URL}/?date={date_str}</id>",
            f"    <title>{escape(title)}</title>",
            f'    <link href="{SITE_URL}/?date={date_str}"/>',
            f"    <updated>{date_str}T12:00:00Z</updated>",
            f"    <summary>{escape(summary)}</summary>",
            "  </entry>",
        ]
    lines.append("</feed>")
    return "\n".join(lines) + "\n"


def main():
    dry_run = "--dry-run" in sys.argv

    manifest = rebuild_manifest()
    feed = rebuild_feed(manifest)

    dates = manifest["dates"]
    print(f"Found {len(dates)} date(s): {', '.join(sorted(dates.keys(), reverse=True)[:5])}")
    for date_str, entries in sorted(dates.items(), reverse=True)[:3]:
        print(f"  {date_str}:")
        for k, v in sorted(entries.items()):
            print(f"    {k}: {v}")

    if dry_run:
        print("\n[DRY RUN] Would write:")
        print(f"  {INDEX_PATH}")
        print(f"  {FEED_PATH}")
        return

    INDEX_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    FEED_PATH.write_text(feed)
    print(f"\nWrote {INDEX_PATH}")
    print(f"Wrote {FEED_PATH}")


if __name__ == "__main__":
    main()
