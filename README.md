# PepeVault — pepevault.lol

Source code for the **[PepeVault](https://pepevault.lol)** traveling Pepe lore exhibition microsite.

## Two-part deliverable

This project ships in two places:

1. **This GitHub repo** — source code: HTML, CSS, JS (inline), markdown docs, tweet pack
2. **[Google Drive folder](https://drive.google.com/drive/folders/1IycNzkSvBxlYTE1Qev5eZyB5wBFhpCRz)** — canonical media bundle: 38 image and video assets (logo, posters, key art, spotlight cards, hype reels)

**Why split?** Git is built for source code, not binaries. Co-locating 70MB of media in this repo would bloat history forever. Standard production practice is to host static media on a CDN / object storage and reference it from the HTML. See `PEPEVAULT-HANDOFF.md` Section 2 for the three deployment paths.

## What is PepeVault?

A curated travelling exhibition that surfaces the real on-chain Pepe lineage — **Rare Pepes · FAKERARES · Notable Pepes · Bitcoin Stamps** — across two cities and three nights in June 2026:

- 📍 **NFC LISBON** · Jun 4–6 · Unicorn Factory Lisboa
- 🟢 **STAMPFEST 3 · The Flock Party** · sponsored by Stampchain.io · secret Lisbon location
- 📍 **PEPEX PRAGUE** · Jun 11 · Fuchs2 · Štvanice Island · bar upstairs (warmup × 600000000000.com)

## Repo contents

```
pepevault-lol/
├── README.md                      ← this file
├── LICENSE                        ← MIT
├── .gitignore
├── PEPEVAULT-HANDOFF.md           ← full deployer instructions (start here)
├── pepevault.html                 ← main site
├── pepevault-presskit.html        ← 10-page press kit (Save-as-PDF ready)
├── pepevault-live.html            ← live stream teaser page
├── pepevault-tweets.md            ← social media post pack
└── v30-backup/                    ← pre-v31 snapshots (rollback safety)
```

**Media assets** load from `pub.hyperagent.com` URLs inside the HTML. Those URLs are stable. To self-host the media, download the `/media/` folder from the [Drive folder](https://drive.google.com/drive/folders/1IycNzkSvBxlYTE1Qev5eZyB5wBFhpCRz) and follow Path 2 or Path 3 in `PEPEVAULT-HANDOFF.md` Section 2.

## Deploying

This is a static site — no build step, no dependencies. Drop the HTML on any static host:

```
pepevault.lol/
├── index.html       ← pepevault.html, renamed
├── live/index.html  ← pepevault-live.html, renamed
└── press/index.html ← pepevault-presskit.html, renamed
```

**Recommended hosts:** Cloudflare Pages · Vercel · Netlify (free tiers cover this site's scale).

Full step-by-step in **`PEPEVAULT-HANDOFF.md`**.

## The Manifold mint widget

The Hall of Memes mint flow uses a CTA card that opens [manifold.xyz](https://manifold.xyz/@ditacrypto/id/4053440752) in a new tab. To upgrade to an on-site deep-embed widget, see **Section 4 of the handoff doc** — you'll register a Manifold Studio app, drop in a client_id, and un-comment two blocks in `pepevault.html`.

## Brand notes (don't break these)

- The word "NFT" is never used in PepeVault copy — it's **digital collectible** or **digital token**.
- Fake Tickets are intentionally absurd / non-deliverable folklore. Only the **Vaultmaster** tier promises real on-site artist merch.
- Sponsor names: **FAKERARES** (one word) is canonical.
- Roster URL conventions are mostly `pepe.wtf/artists/{slug}` with four documented exceptions — see Section 9 of the handoff doc.

## Real assets. Real artists. Real chaos.

🐸 `@PepeVault1` · hello@pepevault.lol
