# PEPEVAULT — Technical Handoff Doc

Everything the person who handles the custom-domain migration needs.

---

## TL;DR — WHAT YOU'RE INHERITING

A complete, working three-page brand microsite + 30+ public assets, currently live on temporary Hyperagent share URLs. Your job: move it to `pepevault.xyz` so the URLs are clean and social previews work properly.

Effort: 1-2 hours assuming you're comfortable with Vercel/Netlify/Cloudflare Pages.

---

## 1. WHAT EXISTS

Three HTML pages and a tweet pack:

| File | Source path | Currently at |
|---|---|---|
| **Main site** | `pepevault.html` | https://hyperagent.com/s/uvStTgkB_dHnEWifEjp3SA |
| **Live preview** | `pepevault-live.html` | https://hyperagent.com/s/kRyvMbSf9SIbp3W6jjJZOQ |
| **Press kit** | `pepevault-presskit.html` | https://hyperagent.com/s/W98ggljH7VbD_rH-3CDmHQ |
| **Tweet pack** | `pepevault-tweets.md` | https://pub.hyperagent.com/api/published/pbf01KRVK7QEV_9DNSBMRPHFR873TQ/pepevault-tweets.md |

All three HTML files are self-contained (no build step, no node_modules, no framework). Just HTML + inline CSS + inline JS + external Google Fonts + external `pub.hyperagent.com` asset URLs.

---

## 2. THE ASSET URLS (the embedded images/videos)

All assets are publicly hosted on `pub.hyperagent.com` and referenced inside the HTML files via `<img src>` and `<source src>` tags. You can **leave these URLs as-is** during the migration — they're permanent and reliable. The site will work perfectly with these URLs even after you switch domains.

If you'd rather self-host the assets too, download them all and update the URLs. List of every asset URL is in the **state snapshot memory** (search for "PEPEVAULT — Current State Snapshot" in the agent's memory).

Categories of assets:
- Brand logo SVG (one variant currently used)
- Hero image (user's cover.jpeg)
- Lineup poster v2
- 2 event key art images (NFC Lisbon, PEPEX Prague)
- 2 hype reel videos (8s each, 1080p)
- 4 sponsor thank-you graphics (FAKERARES, Notable Pepes, Northern Satoshi, Stampchain)
- 4 Counterparty reward cards (VAULT KEY, TICKET STUB, LISBOA FROG, PRAGUE FROG)
- 13 artist spotlight cards (one per roster member)
- 2 live page graphics (broadcast hero, offline state)
- 7 countdown frames (T-7 through T-1)

Total: ~36 images + 2 videos. All on pub.hyperagent.com.

---

## 3. MIGRATION TO PEPEVAULT.XYZ

### Step A — Register the domain
- Suggested registrars: **Porkbun** (cheapest for .xyz), **Cloudflare Registrar** (at-cost), **Namecheap**
- Cost: ~$2-12 first year

### Step B — Choose a host
Pick any static host. All are free for this site's scale:
- **Vercel** (easiest if using GitHub) → drag-and-drop folder also works
- **Netlify** (similar, drag-and-drop deploy)
- **Cloudflare Pages** (integrates well with their registrar)

### Step C — Deploy the files
Create this folder structure on the host:

```
pepevault.xyz/
├── index.html           ← rename pepevault.html → index.html
├── live/
│   └── index.html       ← rename pepevault-live.html → live/index.html
├── press/
│   └── index.html       ← rename pepevault-presskit.html → press/index.html
└── (optional)
    └── tweets.md        ← pepevault-tweets.md if you want it hosted
```

### Step D — Update internal links

Once deployed, update the `<a href>` tags inside the HTML to use clean paths:

In `pepevault.html` (main site):
- Replace `https://hyperagent.com/s/kRyvMbSf9SIbp3W6jjJZOQ` → `/live`
- Replace `https://hyperagent.com/s/W98ggljH7VbD_rH-3CDmHQ` → `/press`
- Both appear multiple times (nav link + WATCH LIVE button + Prague event card + press kit download)

In `pepevault-live.html`:
- Replace `https://pepevault.xyz` → `/` for the back-to-main links (or keep absolute if you want)

In `pepevault-presskit.html`:
- Replace `https://pepevault.xyz` → `/` for back-to-main links

(Use find-and-replace in any editor — the search strings are unique enough.)

### Step E — DNS
Point `pepevault.xyz` at your host. Each host has docs:
- Vercel: Add domain in project settings → set A record to 76.76.21.21 or use their nameservers
- Netlify: Same pattern, their docs are clear
- Cloudflare Pages: Auto if you registered through Cloudflare

### Step F — SSL
Auto-provisioned by all three hosts. Don't need to do anything manual.

---

## 4. KNOWN LIMITATIONS BEING FIXED BY MIGRATION

Once on `pepevault.xyz`, three things automatically improve:

1. **Social link previews:** Currently `hyperagent.com/s/...` URLs wrap with their own OG metadata, so X/Telegram/iMessage previews show "Made with Hyperagent". After migration, the proper PepeVault OG image + title + description take over. The schema markup we added will also kick in.

2. **Clean URLs:** Instead of `hyperagent.com/s/uvStTgkB_dHnEWifEjp3SA`, just `pepevault.xyz`.

3. **Brandability:** Bookmarks, business cards, signage all work.

---

## 5. POST-MIGRATION TODOs (NICE TO HAVE, NOT BLOCKING)

These can wait or be skipped:

- **Real Twitter timeline embed** in the FOLLOW section. Currently styled "Follow @PepeVault1" card. To swap for real timeline: add Twitter's widget JS (`https://platform.twitter.com/widgets.js`) and replace the `.follow-card` div with `<a class="twitter-timeline" href="https://twitter.com/pepevault1">Tweets by @pepevault1</a>`. The styled card looks better in most cases, but the option's there.

- **PEPORACLE interactive: enable inline mode after migration.** Currently the "▶ ACTIVATE PEPORACLE · NEW TAB" button opens the Arweave-hosted oracle in a new tab. This is because Hyperagent's `pub.hyperagent.com/s/` wrapper sandboxes the page WITHOUT `allow-same-origin`, which breaks the same-origin doc.write() trick that lets the oracle's BTC API fetches work. On a real domain (no outer sandbox), the inline approach works just like tokenscan.io does it. To switch back to inline after deploying to pepevault.xyz: in pepevault.html find the `// PEPORACLE — pragmatic launch in new tab` JS block and uncomment/swap to the alternative `fetch + iframe.contentDocument.write` version (the original inline implementation is documented in the git history; the function signature stays the same). For ditacrypto's preferred experience the inline mode is recommended once available.

- **Real PEPORACLE Counterparty dispenser URL** when distribution opens. Currently the Token section is LIVE with the cp20.tokenscan.io/asset/PEPORACLE link wired up. The interactive Arweave embed loads on click. When you have a dispenser URL, swap the `<a class="address-value">cp20.tokenscan.io/asset/PEPORACLE</a>` in the `<section class="section support">` `<div class="support-block">` (second one, with the `$PEPORACLE` header).

- **Real sponsor logo files** to replace the illustrated thank-you graphics. The illustrated ones look great on-brand though — only swap if a sponsor specifically requests their actual logo be used.

- **Image optimization:** Several PNGs are 2-3MB. Compressing with tinypng / sharp / squoosh would speed up mobile load. Not blocking.

- **404 page:** Optional. Add `404.html` at the root that links back home.

---

## 6. WHAT'S WIRED + READY

The site has working:
- ✓ Mobile-responsive layout
- ✓ Click-to-copy BTC donation address (with sandbox-safe fallback)
- ✓ OpenStreetMap iframe maps for both event venues
- ✓ Real BTC donation address: `1KptKyL5e9oxwecpTFggnTtM2oFZHBq48J`
- ✓ Live ticket purchase links (NFC Summit Eventbrite + 600000000000.com)
- ✓ Mailto sponsor enquiry with pre-filled subject + body
- ✓ Clickable artist cards opening pop-out modals with pepe.wtf + X links
- ✓ Easter egg 🐸 in footer opening hidden roster gallery
- ✓ Countdown timers on live page (auto-switches to "LIVE NOW" when dates pass)
- ✓ Press kit "Save as PDF" button (browser print-to-PDF)
- ✓ Schema.org Event markup for SEO
- ✓ Open Graph + Twitter Card meta tags (will activate after domain migration)

---

## 7. CONTACT POINTS / WHO OWNS WHAT

- **X account:** @PepeVault1 (the project owns)
- **Email shown on site:** hello@pepevault.xyz — needs to be set up at registrar's email forwarding or Google Workspace
- **BTC donation address:** `1KptKyL5e9oxwecpTFggnTtM2oFZHBq48J` (project's wallet)
- **Sponsorship enquiries:** mailto goes to hello@pepevault.xyz (set up forwarding)
- **Press kit + Brand assets:** see asset URLs section

---

## 8. WHAT WAS BUILT (so you know what you're inheriting)

Across the build session(s):
- Complete brand identity from a user-provided logo + cover image
- 17+ versions of the main site iterated through
- A full press kit with 8 print-ready pages
- A live stream teaser page with dual countdown timers
- 36 illustrated brand assets (lineup poster, key art, hype reels, reward cards, sponsor graphics, spotlight cards, countdown frames, live-page hero, offline state)
- Tweet pack covering manifesto, roster spotlights, sponsor thank-yous, countdown, lottery hook, Prague pivot

Total scope: 30+ tool-orchestrated generation/editing turns plus careful pipeline work to ensure all assets are on public URLs that work outside the Hyperagent platform.

---

## 9. IF YOU NEED TO REGENERATE OR EDIT

The original source files are in the agent's workspace. The agent can resume the build any time — search the agent's memory for "PEPEVAULT — Current State Snapshot" which has all artifact IDs, URLs, and remaining tasks indexed.

Critical constraints documented (don't violate):
- Meme Conscious's real name is private (PII)
- Spotlight cards (13) are X teasers, NOT Counterparty assets
- Reward cards (4) ARE intended as Counterparty assets
- Sponsor names: FAKERARES (one word) is canonical

---

Real assets. Real artists. Real chaos.
DYOR · Touch grass · Trade Pepes 🐸

— Generated as part of the PepeVault build session, May 2026
