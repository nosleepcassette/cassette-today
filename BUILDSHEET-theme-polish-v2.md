# BUILDSHEET — cassette-today: amber default, CRT polish, full nav, media folder
# maps · cassette.help · MIT
# Target: Codex
# Date: 2026-04-30
# File: ~/dev/cassette-today/BUILDSHEET-theme-polish-v2.md

---

## Context & what's already done (do NOT redo)

- `samples.html` oracle report section: 7-section card grid already built. Images
  still at root level — media folder task below will move them.
- Old intro image removed from samples manually.
- `index.html` code fence fix for hexagram ASCII rendering: already done.
- `readings/index.json` and `feed.xml` already rebuilt and pushed.
- `samples.html` still uses the wrong localStorage key (`'theme'` instead of
  `'nsc-theme'`) — fix in Task 3.

Files you will touch:
- `index.html`, `archive.html`, `samples.html`, `about.html` — all four
- File system: `media/oracle-report/` folder

---

## Task 1 — Media folder: move oracle report images

### 1a. Create folder
```bash
mkdir -p ~/dev/cassette-today/media/oracle-report
```

### 1b. Copy fresh images FROM ATLAS (these are canonical source of truth)

```bash
cd ~/atlas/readings/showcase/render.out/

cp oracle-report-maps-2026-04-28-public-mapsvoice-the-oracle-report-maps.png \
   ~/dev/cassette-today/media/oracle-report/

# NOTE: intro uses the -intro-single.png variant, renamed to intro.png
cp oracle-report-maps-2026-04-28-public-mapsvoice-intro-single.png \
   ~/dev/cassette-today/media/oracle-report/oracle-report-maps-2026-04-28-public-mapsvoice-intro.png

cp oracle-report-maps-2026-04-28-public-mapsvoice-who-you-are-natal-architecture.png \
   ~/dev/cassette-today/media/oracle-report/

cp oracle-report-maps-2026-04-28-public-mapsvoice-what-the-cards-say-tarot.png \
   ~/dev/cassette-today/media/oracle-report/

cp oracle-report-maps-2026-04-28-public-mapsvoice-what-the-oracle-tracks-i-ching.png \
   ~/dev/cassette-today/media/oracle-report/

cp oracle-report-maps-2026-04-28-public-mapsvoice-what-the-sky-is-doing-astrologic.png \
   ~/dev/cassette-today/media/oracle-report/

cp oracle-report-maps-2026-04-28-public-mapsvoice-the-full-synthesis.png \
   ~/dev/cassette-today/media/oracle-report/
```

### 1c. Update samples.html image paths

In `samples.html`, find every `src="./oracle-report-maps-2026-04-28-public-mapsvoice-*.png"`
and every `onclick="window.open('./oracle-report-maps-...')"`.

Change all paths: `./oracle-report-maps-...` → `./media/oracle-report/oracle-report-maps-...`

The root-level combined single PDF link (`./oracle-report-maps-2026-04-28-public-single.png`)
is a different file — leave it at root, do not move it.

### 1d. Remove old root-level PNGs (after updating paths)

```bash
cd ~/dev/cassette-today
git rm -f oracle-report-maps-2026-04-28-public-mapsvoice-intro.png \
          oracle-report-maps-2026-04-28-public-mapsvoice-the-oracle-report-maps.png \
          oracle-report-maps-2026-04-28-public-mapsvoice-who-you-are-natal-architecture.png \
          oracle-report-maps-2026-04-28-public-mapsvoice-what-the-cards-say-tarot.png \
          oracle-report-maps-2026-04-28-public-mapsvoice-what-the-oracle-tracks-i-ching.png \
          oracle-report-maps-2026-04-28-public-mapsvoice-what-the-sky-is-doing-astrologic.png \
          oracle-report-maps-2026-04-28-public-mapsvoice-the-full-synthesis.png \
          2>/dev/null; true
```

---

## Task 2 — Remove all cyan, make amber the root default

Apply to ALL FOUR files: `index.html`, `archive.html`, `samples.html`, `about.html`

### 2a. Change `:root` color vars in each file

Every file has a `:root { ... }` block. Find this pattern (accent may already be
amber in some files — check before editing):

```css
:root {
  --bg: #05070a; --fg: #e9feff; --dim: rgba(233,254,255,.65);
  --accent: #4bf4ff; --muted: rgba(75,244,255,.45);
  --glow: rgba(75,244,255,.22); --glow2: rgba(75,244,255,.08);
  --border: rgba(75,244,255,.25);
  --anag-r: rgba(250,74,51,.62); --anag-c: rgba(71,184,184,.42);
  ...
}
```

Replace color vars with amber:
```css
:root {
  --bg: #05070a; --fg: #e9feff; --dim: rgba(233,254,255,.65);
  --accent: #ffb000; --muted: rgba(255,176,0,.45);
  --glow: rgba(255,176,0,.22); --glow2: rgba(255,176,0,.08);
  --border: rgba(255,176,0,.25);
  --anag-r: rgba(255,60,0,.5); --anag-c: rgba(200,140,0,.4);
  --scan: .065; --bar-h: 22px; --font: 'VT323', 'Courier New', monospace;
}
```

### 2b. Delete the `[data-theme="amber"]` override block (now redundant)

In each file, find and delete this block entirely:
```css
:root[data-theme="amber"] {
  --accent: #ffb000; --muted: rgba(255,176,0,.45);
  --glow: rgba(255,176,0,.22); --glow2: rgba(255,176,0,.08);
  --border: rgba(255,176,0,.25); --anag-r: rgba(255,60,0,.5); --anag-c: rgba(200,140,0,.4);
}
```

### 2c. Replace hardcoded cyan rgba values in CSS (NOT inside other theme blocks)

Only replace values that appear OUTSIDE of `[data-theme="green"]`,
`[data-theme="trans"]`, and `[data-theme="lesbian"]` blocks.

Replacements:
```
rgba(75,244,255,.04)  →  rgba(255,176,0,.04)
rgba(75,244,255,.05)  →  rgba(255,176,0,.05)
rgba(75,244,255,.06)  →  rgba(255,176,0,.06)
rgba(75,244,255,.07)  →  rgba(255,176,0,.07)
rgba(75,244,255,.08)  →  rgba(255,176,0,.08)
rgba(75,244,255,.10)  →  rgba(255,176,0,.10)
rgba(75,244,255,.12)  →  rgba(255,176,0,.12)
rgba(75,244,255,.15)  →  rgba(255,176,0,.15)
rgba(75,244,255,.22)  →  rgba(255,176,0,.22)
rgba(75,244,255,.25)  →  rgba(255,176,0,.25)
rgba(75,244,255,.28)  →  rgba(255,176,0,.28)
rgba(75,244,255,.30)  →  rgba(255,176,0,.30)
rgba(75,244,255,.45)  →  rgba(255,176,0,.45)
```

Also replace in the favicon SVG `stroke='%234bf4ff'` with `stroke='%23ffb000'` in
each file's `<link rel="icon">` tag:
```
stroke='%234bf4ff'  →  stroke='%23ffb000'
```

### 2d. Remove cyan from theme cycle and help panels

In each file's JS, remove `'cyan'` from the valid themes array and remove the
`if (t === 'cyan')` special-case branch.

**Archive.html JS — find:**
```javascript
var valid = ['cyan','amber','green','trans','lesbian'];
if (valid.indexOf(t) === -1) return;
localStorage.setItem('nsc-theme', t);
if (t === 'cyan') document.documentElement.removeAttribute('data-theme');
else document.documentElement.setAttribute('data-theme', t);
```
**Replace with:**
```javascript
var valid = ['amber','green','trans','lesbian'];
if (valid.indexOf(t) === -1) return;
localStorage.setItem('nsc-theme', t);
document.documentElement.setAttribute('data-theme', t);
```

**Archive.html JS — also fix initial load (find):**
```javascript
var savedTheme = localStorage.getItem('nsc-theme') || 'amber';
if (savedTheme !== 'cyan') document.documentElement.setAttribute('data-theme', savedTheme);
```
**Replace with:**
```javascript
var savedTheme = localStorage.getItem('nsc-theme') || 'amber';
document.documentElement.setAttribute('data-theme', savedTheme);
```

In each file's **help overlay HTML**, remove the cyan row:
```html
<div class="help-row"><span class="key">:theme cyan</span><span class="help-desc">default cyan</span></div>
```

In each file's **JS command handler**, remove the `cyan` case from `:theme` handling.

### 2e. Fix samples.html localStorage key mismatch

In `samples.html`, the JS uses `'theme'` instead of `'nsc-theme'`. Find:
```javascript
localStorage.getItem('theme')
localStorage.setItem('theme', t)
var savedTheme = localStorage.getItem('theme') || '';
if (savedTheme) applyTheme(savedTheme);
```
Replace all occurrences with:
```javascript
localStorage.getItem('nsc-theme')
localStorage.setItem('nsc-theme', t)
var savedTheme = localStorage.getItem('nsc-theme') || 'amber';
applyTheme(savedTheme);
```

---

## Task 3 — CRT aesthetic upgrade

Apply to `index.html` (primary), and mirror the CSS-only changes to the other 3 files.

### 3a. Fix: banner/text dim under effects

**Problem:** At fx 2+ (CRT/VHS/chaos), the scanline overlay and vignette wash out
the banner art and card names, making them dim and unreadable.

**Fix:** At higher fx levels, boost banner and card-name glow to punch through.

In each file, find:
```css
:root[data-fx="3"] .banner-art,
:root[data-fx="4"] .banner-art,
:root[data-fx="3"] .banner-mobile-inner,
:root[data-fx="4"] .banner-mobile-inner {
  text-shadow: 0 0 12px var(--glow), 0 0 36px var(--glow2), 0 0 60px var(--glow2);
}
:root[data-fx="3"] .card-name,
:root[data-fx="4"] .card-name {
  text-shadow: 0 0 30px var(--glow), 0 0 60px var(--glow2);
}
```

Replace with:
```css
/* fx2: CRT — gentle boost */
:root[data-fx="2"] .banner-art,
:root[data-fx="2"] .banner-mobile-inner {
  text-shadow: 0 0 6px var(--glow), 0 0 18px var(--glow), 0 0 40px var(--glow2);
  filter: brightness(1.15);
}
:root[data-fx="2"] .card-name {
  text-shadow: 0 0 14px var(--glow), 0 0 32px var(--glow2);
  filter: brightness(1.1);
}
/* fx3/4: VHS + chaos — strong boost to stay readable */
:root[data-fx="3"] .banner-art,
:root[data-fx="4"] .banner-art,
:root[data-fx="3"] .banner-mobile-inner,
:root[data-fx="4"] .banner-mobile-inner {
  text-shadow: 0 0 8px var(--glow), 0 0 24px var(--glow), 0 0 50px var(--glow), 0 0 80px var(--glow2);
  filter: brightness(1.3);
}
:root[data-fx="3"] .card-name,
:root[data-fx="4"] .card-name {
  text-shadow: 0 0 20px var(--glow), 0 0 40px var(--glow), 0 0 70px var(--glow2);
  filter: brightness(1.2);
}
/* General text at fx3/4: compensate for vignette/scan wash */
:root[data-fx="3"] .reading-body,
:root[data-fx="4"] .reading-body {
  filter: brightness(1.1);
}
```

### 3b. Enhanced ambient glow on body background

In `index.html` (and mirror to other 3), the body has two radial gradient blobs.
Add a third subtle mid-screen glow for depth, and make the existing ones slightly
stronger:

Find the body background rule:
```css
body {
  ...
  background:
    radial-gradient(1100px 700px at 38% 28%, var(--glow), transparent 62%),
    radial-gradient(800px 500px at 72% 72%, rgba(75,244,255,.05), transparent 58%),
    var(--bg);
```

Replace (note: the second gradient uses hardcoded cyan — fix to amber var too):
```css
body {
  ...
  background:
    radial-gradient(1100px 700px at 38% 28%, var(--glow), transparent 62%),
    radial-gradient(900px 600px at 72% 72%, var(--glow2), transparent 58%),
    radial-gradient(600px 400px at 50% 50%, rgba(255,176,0,.03), transparent 55%),
    var(--bg);
```

### 3c. Add persistent low-level scanline to fx2 (CRT default)

The current CRT scanlines only show via `--scan: .065`. Add a secondary very-fine
horizontal scan texture via a second `body::after` pseudo-element that's always
present at fx2+:

```css
/* Fine phosphor texture — visible at fx2+ */
body::after {
  content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 201;
  background: repeating-linear-gradient(
    to bottom,
    transparent 0px, transparent 1px,
    rgba(0,0,0,.04) 1px, rgba(0,0,0,.04) 2px
  );
  opacity: 0; transition: opacity .4s;
}
:root[data-fx="2"] body::after { opacity: 1; }
:root[data-fx="3"] body::after { opacity: 1; }
:root[data-fx="4"] body::after { opacity: 1; }
:root[data-fx="0"] body::after,
:root[data-fx="1"] body::after { opacity: 0; }
```

### 3d. Subtle text glow on body text at fx2+

Normal paragraph text should have a very faint amber bloom at CRT level:

```css
:root[data-fx="2"] .reading-body,
:root[data-fx="3"] .reading-body,
:root[data-fx="4"] .reading-body {
  text-shadow: 0 0 6px rgba(255,176,0,.12);
}
:root[data-fx="2"] .tui-nav a,
:root[data-fx="3"] .tui-nav a,
:root[data-fx="4"] .tui-nav a {
  text-shadow: 0 0 8px rgba(255,176,0,.20);
}
```

### 3e. Periodic glitch animation on banner (fx2 only — subtle)

The banner already has a `banner-glitch` animation that fires once on load. Add a
slow repeating subtle glitch that fires at CRT level (fx2):

```css
@keyframes banner-idle-glitch {
  0%, 91%, 100% { transform: none; filter: brightness(1); }
  92%  { transform: translateX(1px) scaleX(1.001); filter: brightness(1.05); }
  93%  { transform: translateX(-1px); }
  94%  { transform: none; }
  96%  { transform: translateX(.5px); filter: brightness(1.02); }
  97%  { transform: none; filter: brightness(1); }
}
:root[data-fx="2"] .banner-art {
  animation: banner-glitch 1.1s ease-out forwards,
             banner-idle-glitch 14s ease-in-out 2s infinite;
}
```

At fx3/fx4, the existing chaos-glitch JS already handles this — don't add the
idle animation there.

### 3f. Slightly brighter nav links and status hint

In all 4 files (these are element-level CSS, same across all pages):

```css
/* FIND: */
.tui-nav a { color: var(--dim); ... }
/* REPLACE with: */
.tui-nav a { color: rgba(233,254,255,.90); ... }

/* FIND: */
.tui-nav .nav-sep { color: var(--border); ... }
/* REPLACE with: */
.tui-nav .nav-sep { color: rgba(233,254,255,.40); ... }

/* FIND: */
.tui-title { color: var(--dim); ... }
/* REPLACE with: */
.tui-title { color: rgba(233,254,255,.82); ... }

/* FIND: */
.status-hint { color: rgba(233,254,255,.30); ... }
/* REPLACE with: */
.status-hint { color: rgba(233,254,255,.55); ... }
```

---

## Task 4 — Full nav: every page links to all others

### 4a. Standardize top nav bar on all 4 pages

All 4 pages must have identical nav: `today · archive · samples · about`

**Current missing links:**
- `index.html` nav: check — should have all 4 ✓
- `archive.html` nav: check — should have all 4 ✓
- `samples.html` nav: check — should have all 4 ✓
- `about.html` nav: check — should have all 4 ✓

If any are missing, add the missing links. The pattern is:
```html
<nav class="tui-nav" aria-label="Site navigation">
  <a href="index.html">today</a>
  <span class="nav-sep">·</span>
  <a href="archive.html">archive</a>
  <span class="nav-sep">·</span>
  <a href="samples.html">samples</a>
  <span class="nav-sep">·</span>
  <a href="about.html">about</a>
</nav>
```

Mark the current page with `class="active" aria-current="page"`.

### 4b. Standardize footer on all 4 pages

Every footer must have: `today · archive · samples · about · rss · ko-fi`

Canonical footer (apply to all 4 files):
```html
<footer class="tui-footer" role="contentinfo">
  <a href="index.html">today</a>
  <span class="sep">·</span>
  <a href="archive.html">archive</a>
  <span class="sep">·</span>
  <a href="samples.html">samples</a>
  <span class="sep">·</span>
  <a href="about.html">about</a>
  <span class="sep">·</span>
  <a href="feed.xml">rss</a>
  <span class="sep">·</span>
  <a href="https://ko-fi.com/nosleepcassette" target="_blank" rel="noopener">ko-fi</a>
</footer>
```

### 4c. Standardize command palette navigation in all 4 files

All 4 files should respond to `:today`, `:archive`, `:samples`, `:about`, `:kofi`
in the command overlay. Find the JS command handler block in each file and ensure
all 5 are present:

```javascript
if (cmd === 'today') { window.location.href = 'index.html'; return; }
if (cmd === 'archive') { window.location.href = 'archive.html'; return; }
if (cmd === 'samples') { window.location.href = 'samples.html'; return; }
if (cmd === 'about') { window.location.href = 'about.html'; return; }
if (cmd === 'kofi') { window.open('https://ko-fi.com/nosleepcassette', '_blank'); return; }
```

---

## Task 5 — Archive: date entries as real links

In `archive.html`, the `makeRow()` function creates `<div>` elements. Change to `<a>`
so they are right-clickable, deep-linkable, and properly accessible.

### 5a. CSS: add no-underline/inherit-color to `.date-entry`

Find the `.date-entry` CSS rule and add:
```css
text-decoration: none; color: inherit;
```

### 5b. JS: `makeRow()` — use `<a>` not `<div>`

Find:
```javascript
function makeRow(entry) {
  var row = document.createElement('div');
  row.className = 'date-entry';
  row.setAttribute('role', 'listitem');
  row.setAttribute('tabindex', '0');
  row.setAttribute('data-date', entry.date);
  ...
  row.addEventListener('click', function() { openDate(entry.date); });
  return row;
}
```

Replace with:
```javascript
function makeRow(entry) {
  var row = document.createElement('a');
  row.href = '#' + entry.date;
  row.className = 'date-entry';
  row.setAttribute('role', 'listitem');
  row.setAttribute('data-date', entry.date);
  var cardLabel = entry.cards ? entry.cards.join(' · ') : 'reading available';
  row.setAttribute('aria-label', formatDateDisplay(entry.date) + ', ' + entry.count + ' readings');
  row.innerHTML =
    '<span class="date-key">' + entry.date + '</span>' +
    '<span class="date-cards">' + cardLabel + '</span>' +
    '<span class="date-count">' + entry.count + '/3</span>';
  row.addEventListener('click', function(e) { e.preventDefault(); openDate(entry.date); });
  return row;
}
```

---

## Task 6 — Smoke tests

```bash
# Verify no cyan color values remain in root/default CSS (outside theme blocks)
grep -n "4bf4ff" ~/dev/cassette-today/index.html | grep -v "data-theme"
# Should return nothing (or only theme-block entries)

# Verify images are in media folder and samples.html references them
ls ~/dev/cassette-today/media/oracle-report/*.png | wc -l
# Should be 7

grep "media/oracle-report" ~/dev/cassette-today/samples.html | wc -l
# Should be 14+ (2 refs per image: src + onclick)

# Visual: open each page in browser, verify amber default, no cyan, nav complete
# Check fx2 (CRT) — banner should be clearly readable, have faint idle glitch
# Check fx3/fx4 — banner should be even brighter/more readable, not washed out
```

---

## Task 7 — Git commit and push

```bash
cd ~/dev/cassette-today
git add -A -- ':!*.DS_Store' ':!conversation-*.txt' ':!BUILDSHEET*.md'
git commit -m "theme: amber default, CRT glow polish, full nav, archive links, media folder"
git push origin main
```

---

## Feature upgrade plan (future buildsheets — do NOT implement now)

### Near-term (next buildsheet)

1. **Reading share card** — when `index.html` loads a specific reading, og:image
   dynamically points to that day's oracle report PNG (if it exists). Enables
   preview-rich sharing.

2. **Reading deep-link copy button** — in the archive viewer, a small `[ copy link ]`
   button that copies `cassette.help/#YYYY-MM-DD` to clipboard. Makes sharing any
   day trivial.

3. **Today page: date-aware loading** — currently today's reading is hardcoded/latest.
   Add `?date=YYYY-MM-DD` query param support so any archived reading can be viewed
   in the full today-page layout (with hexagram art, styled sections, etc).

4. **Progressive image loading** — oracle report section cards are 1–3MB each.
   IntersectionObserver-based lazy shimmer so page feels instant on load.

5. **RSS feed in top nav** — add `rss` link to the nav bar (currently only in footer).

### Mid-term

6. **About page: augury/pipeline section** — brief section on the augury system with
   GitHub link and a note on the oracle report pipeline. Currently the about page
   doesn't explain how readings are generated.

7. **Mobile: oracle card swipe** — on narrow screens, the 7-card oracle section could
   be a horizontal scroll carousel rather than a 2-col grid.

8. **Samples: more reading types** — add celtic cross standalone and natal essentials
   examples to fill the two remaining "coming soon" placeholders.

9. **Search across readings** — archive search currently filters by card name/date.
   Full-text search against the `.website.md` reading files (fetched on demand) would
   let visitors search by hexagram, concept, keyword.

10. **Ko-fi tier descriptions on about** — currently about has tiers listed. A small
    visual tier card component with "book now" buttons per tier would convert better.

### Longer-term

11. **Daily email/RSS** — auto-generated RSS already exists (`feed.xml`). An email
    digest (Buttondown or Mailchimp) fed from the same pipeline would extend reach.

12. **Reading archive calendar view** — month-grid view on archive page, days with
    readings highlighted. Click a day → reading. Feels more like a journal.

13. **Dark/light toggle** — current themes are all dark. Some users prefer light.
    A `--bg: #f5f0e8` parchment variant with `--accent: #8b4513` (sepia) as a 5th
    theme option.

14. **Public reading subscription** — form on about/samples page where visitors
    enter email to receive the daily public reading. Can start as a simple Mailchimp
    embed, no infrastructure needed.

---
*maps · cassette.help · MIT*
