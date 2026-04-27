#!/usr/bin/env python3
# maps · cassette.help · MIT
# Daily reading generator for cassette-today GitHub Pages site.
#
# What this does:
#   1. Runs augury to pull today's card
#   2. Generates a 3-paragraph reading in maps' voice using Hermes/Claude
#   3. Renders new index.html from template
#   4. Git commits and pushes to GitHub Pages repo
#
# Usage:
#   python3 generate.py                  # generate + push
#   python3 generate.py --dry-run        # generate only, print result, no push
#   python3 generate.py --push-only      # skip generation, just git push
#
# Cron (add to crontab -e):
#   0 8 * * * cd ~/dev/cassette-today && python3 generate.py >> ~/.hermes/logs/cassette-today.log 2>&1

import os
import re
import sys
import json
import random
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from string import Template

# ── CONFIG ──────────────────────────────────────────────────────────────────

REPO_DIR   = Path(__file__).parent.resolve()
TEMPLATE   = REPO_DIR / "index.template.html"
OUTPUT     = REPO_DIR / "index.html"
LOG_DIR    = Path(os.path.expanduser("~/.hermes/logs"))
READING_CACHE = Path(os.path.expanduser("~/.hermes/data/cassette-today-cache.json"))

# Hermes skill or fallback model for caption generation
HERMES_CMD = os.getenv("HERMES_CMD", "hermes")

# ── AUGURY ──────────────────────────────────────────────────────────────────

def pull_daily_card() -> dict:
    """Run augury daily pull, return structured data."""
    try:
        result = subprocess.run(
            ["python3", "-m", "augury", "read",
             "--spread", "single", "--json", "--no-save"],
            capture_output=True, text=True, timeout=30,
            cwd=Path(os.path.expanduser("~/dev/augury"))
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            # augury JSON schema: cards list, each has name, reversed, meaning, etc.
            cards = data.get("cards") or data.get("drawn_cards") or []
            if cards:
                card = cards[0]
                return {
                    "name": card.get("name", "Unknown"),
                    "reversed": card.get("reversed", False),
                    "meaning": card.get("meaning", ""),
                    "keywords": card.get("keywords", []),
                    "raw": data,
                }
    except Exception as e:
        print(f"[augury] error: {e}", file=sys.stderr)

    # fallback: try augury daily command
    try:
        result = subprocess.run(
            ["python3", "-m", "augury", "daily", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=Path(os.path.expanduser("~/dev/augury"))
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            cards = data.get("cards") or data.get("drawn_cards") or []
            if cards:
                card = cards[0]
                return {
                    "name": card.get("name", "Unknown"),
                    "reversed": card.get("reversed", False),
                    "meaning": card.get("meaning", ""),
                    "keywords": card.get("keywords", []),
                    "raw": data,
                }
    except Exception as e:
        print(f"[augury daily] error: {e}", file=sys.stderr)

    return {"name": "The Fool", "reversed": False, "meaning": "", "keywords": []}


# ── CAPTION GENERATION ───────────────────────────────────────────────────────

CAPTION_SYSTEM = """You are writing the daily oracle entry for cassette.help in maps' voice.

maps' voice: direct, dry, zero filler. Divination without the crystals-and-good-vibes framing.
Technical precision meets the uncanny. She writes like she talks — fragments for impact,
no rhetorical warmup, occasional profanity when it earns its keep. Never "the universe is
guiding you." More like "the card pulled itself."

Write 3 short paragraphs (2-4 sentences each) about today's card for a public daily reading page.
- Para 1: what the card is and what it's doing today specifically
- Para 2: the uncomfortable part — what it's pointing at
- Para 3: the practical implication. Not advice, just what this means

Do NOT include: the card name as a heading, bullet points, markdown, "today's reading:", or
any preamble. Just the 3 paragraphs. Plain prose. No line breaks between sentences within a paragraph.

Output format: JSON with key "paragraphs" containing a list of 3 strings."""

def generate_caption(card: dict) -> list[str]:
    """Generate 3-paragraph reading caption via Hermes or Claude API."""
    card_display = card["name"]
    if card.get("reversed"):
        card_display += " (reversed)"
    keywords = ", ".join(card.get("keywords", [])[:4]) or "see posting"

    prompt = f"""Card: {card_display}
Keywords: {keywords}
Meaning note: {card.get('meaning', '')[:300]}

Write the 3 paragraphs for today's cassette.help daily reading."""

    # Try Hermes first
    try:
        result = subprocess.run(
            [HERMES_CMD, "--skill", "maps-voice", "--json", prompt],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            paras = data.get("paragraphs") or data.get("content")
            if isinstance(paras, list) and len(paras) >= 3:
                return paras[:3]
    except Exception:
        pass

    # Try Claude API directly
    try:
        import anthropic
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=CAPTION_SYSTEM,
            messages=[{"role": "user", "content": prompt}]
        )
        text = msg.content[0].text
        data = json.loads(text)
        paras = data.get("paragraphs", [])
        if len(paras) >= 3:
            return paras[:3]
    except Exception as e:
        print(f"[claude] caption error: {e}", file=sys.stderr)

    # Fallback: use the card meaning directly
    meaning = card.get("meaning", "")
    if meaning:
        return [
            meaning[:200] + ("..." if len(meaning) > 200 else ""),
            "the cards don't explain themselves. they show up and wait.",
            "check back tomorrow.",
        ]
    return [
        f"{card['name']} pulled today.",
        "the oracle is loading.",
        "full reading available via ko-fi.",
    ]


# ── TEMPLATE RENDERING ───────────────────────────────────────────────────────

def load_template() -> str:
    """Load HTML template. Falls back to index.html if no separate template."""
    if TEMPLATE.exists():
        return TEMPLATE.read_text()
    # Use index.html as template (replace placeholder markers)
    return OUTPUT.read_text()


def render_html(card: dict, paragraphs: list[str], generated_at: datetime) -> str:
    """Render full index.html with today's reading injected."""
    html = load_template()

    date_str = generated_at.strftime("%Y-%m-%d")
    date_display = generated_at.strftime("%B %-d, %Y").lower()

    card_display = card["name"].upper()
    if card.get("reversed"):
        card_display += " · REVERSED"

    paras_html = "\n".join(f"      <p>{_escape(p)}</p>" for p in paragraphs)

    # Replace placeholder markers in the template
    replacements = {
        # date span
        r'<span id="reading-date">[^<]*</span>': f'<span id="reading-date">{date_display}</span>',
        # card name div — matches multiline with data-text + aria-label attrs
        r'<div class="card-name"[^>]*>.*?</div>':
            (
                f'<div class="card-name" id="card-name"\n'
                f'     data-text="{_escape(card_display)}"\n'
                f'     aria-label="Today\'s card: {_escape(card_display.lower())}">\n'
                f'      {card_display}\n'
                f'    </div>'
            ),
        # reading body div (multiline)
        r'<div class="reading-body" id="reading-body"[^>]*>.*?</div>':
            f'<div class="reading-body" id="reading-body" aria-live="polite">\n{paras_html}\n    </div>',
        # meta description
        r'<meta name="description" content="[^"]*">':
            f'<meta name="description" content="Today\'s oracle reading: {_escape(card["name"])}. Daily tarot + astrology by maps.">',
        # og:title
        r'<meta property="og:title" content="[^"]*">':
            f'<meta property="og:title" content="NO SLEEP CASSETTE · {date_display} · {_escape(card["name"])}">',
        # og:description (first paragraph preview)
        r'<meta property="og:description" content="[^"]*">':
            f'<meta property="og:description" content="{_escape(paragraphs[0][:140])}...">',
    }

    for pattern, replacement in replacements.items():
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)

    return html


def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── CACHE ────────────────────────────────────────────────────────────────────

def load_cache() -> dict:
    if READING_CACHE.exists():
        try:
            return json.loads(READING_CACHE.read_text())
        except Exception:
            pass
    return {}


def save_cache(card: dict, paragraphs: list[str], generated_at: datetime):
    READING_CACHE.parent.mkdir(parents=True, exist_ok=True)
    READING_CACHE.write_text(json.dumps({
        "date": generated_at.strftime("%Y-%m-%d"),
        "card": card,
        "paragraphs": paragraphs,
        "generated_at": generated_at.isoformat(),
    }, indent=2))


def cache_is_fresh(cache: dict) -> bool:
    today = datetime.now().strftime("%Y-%m-%d")
    return cache.get("date") == today


# ── GIT PUSH ─────────────────────────────────────────────────────────────────

def git_push(message: str):
    """Commit and push to GitHub Pages."""
    cmds = [
        ["git", "add", "index.html"],
        ["git", "commit", "-m", message],
        ["git", "push"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            # nothing to commit is fine
            if "nothing to commit" in result.stdout + result.stderr:
                print(f"[git] nothing to commit, skipping push")
                return
            print(f"[git] error running {' '.join(cmd)}: {result.stderr}", file=sys.stderr)
            return
        print(f"[git] {' '.join(cmd[:2])}: ok")


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate daily cassette.help reading page")
    parser.add_argument("--dry-run", action="store_true", help="Print rendered HTML, don't write or push")
    parser.add_argument("--push-only", action="store_true", help="Skip generation, just git push current index.html")
    parser.add_argument("--force", action="store_true", help="Regenerate even if today's cache exists")
    args = parser.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now()

    if args.push_only:
        git_push(f"update: {now.strftime('%Y-%m-%d')} push-only")
        return

    cache = load_cache()
    if cache_is_fresh(cache) and not args.force:
        print(f"[generate] cache fresh for {now.strftime('%Y-%m-%d')}, using cached reading")
        card = cache["card"]
        paragraphs = cache["paragraphs"]
    else:
        print(f"[generate] pulling daily card from augury...")
        card = pull_daily_card()
        print(f"[generate] card: {card['name']}{' (rx)' if card.get('reversed') else ''}")

        print(f"[generate] generating caption...")
        paragraphs = generate_caption(card)
        print(f"[generate] caption ok ({len(paragraphs)} paragraphs)")

        save_cache(card, paragraphs, now)

    html = render_html(card, paragraphs, now)

    if args.dry_run:
        print(html)
        return

    OUTPUT.write_text(html)
    print(f"[generate] wrote {OUTPUT}")

    git_push(f"oracle: {now.strftime('%Y-%m-%d')} · {card['name']}{' rx' if card.get('reversed') else ''}")
    print(f"[generate] done")


if __name__ == "__main__":
    main()
