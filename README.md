# cassette-today

Daily oracle reading page for cassette.help, served via GitHub Pages.

**Live at:** `https://nosleepcassette.github.io/cassette-today/`  
(redirect cassette.help → here while VPS is down)

---

## What it is

A single static HTML page updated daily by a local cron job. Hermes pulls a card from augury, generates 3 paragraphs in maps' voice, renders a new `index.html`, commits, and pushes. GitHub Pages serves it.

No server required. No build step. No JS dependencies. Pure HTML + CSS.

---

## Setup

### 1. Create the GitHub repo

```zsh
cd ~/dev/cassette-today
git init
git remote add origin git@github.com:nosleepcassette/cassette-today.git
git checkout -b main
git add .
git commit -m "init: cassette-today reading page"
git push -u origin main
```

Enable GitHub Pages in repo Settings → Pages → Source: `main` branch, root `/`.

### 2. Install Python deps

```zsh
pip3 install anthropic  # fallback caption generation if Hermes unavailable
```

augury must be importable: `python3 -m augury --help` should work.

### 3. Set up cron

```zsh
crontab -e
```

Add:
```
# cassette-today: daily reading page, random time 7-11am PT
0 9 * * * cd ~/dev/cassette-today && python3 generate.py >> ~/.hermes/logs/cassette-today.log 2>&1
```

For the staggered timing Wizard recommended, replace with:
```
# runs at a random minute between 7am-11am PT (420-660 min from midnight)
0 7 * * * sleep $((RANDOM % 14400)) && cd ~/dev/cassette-today && python3 generate.py >> ~/.hermes/logs/cassette-today.log 2>&1
```

### 4. Point cassette.help

While VPS is down, add a CNAME or redirect:
- GitHub Pages will serve at `nosleepcassette.github.io/cassette-today`
- In Cloudflare/your DNS: add a CNAME `cassette.help → nosleepcassette.github.io`
- Add a `CNAME` file in this repo containing `cassette.help`

---

## Manual run

```zsh
# dry run — see output without writing
python3 generate.py --dry-run

# generate + push
python3 generate.py

# force regenerate even if today's cache exists
python3 generate.py --force

# just push current index.html (if you edited it manually)
python3 generate.py --push-only
```

---

## Files

```
index.html      — the page (gets overwritten daily)
generate.py     — cron script: augury → caption → render → push
README.md       — this file
CNAME           — cassette.help (add this for custom domain)
```

Cache lives at `~/.hermes/data/cassette-today-cache.json`. If augury or caption generation fails, the previous day's reading stays up rather than showing an error.

---

## Wiring into the funnel

Every other stream links here:
- Daily Twitter/X post → cassette.help/today
- Ko-fi listings → "today's reading" link in description
- Newsletter → "this week on cassette.help"
- Every reading delivery email → "today's reading" postscript

---

*maps · cassette.help · MIT*
