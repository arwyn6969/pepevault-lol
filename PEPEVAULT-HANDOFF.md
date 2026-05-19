# PEPEVAULT — Technical Handoff Doc (v31, May 2026)

Everything the person deploying PepeVault to its final domain needs.

---

## TL;DR — WHAT YOU'RE INHERITING

A complete, working four-page brand microsite + tweet pack + 38 public media assets. Drop the source files on any static host, point `pepevault.lol` at it, and you're live.

Effort: 1–2 hours assuming you're comfortable with Vercel / Netlify / Cloudflare Pages.

**A note on Hyperagent branding:** While these files were authored in Hyperagent, **none of the "Made with Hyperagent" branding is baked into the source files themselves**. That branding only appears on the `hyperagent.com/s/...` preview URLs — it's an outer wrapper that Hyperagent adds at view-time. Once you upload the raw HTML to your own domain, that wrapper disappears completely. No stripping required.

---

## 1. WHAT'S IN THE PACKAGE

```
PepeVault — Handoff v31/
├── README.md                        ← short deployer summary
├── PEPEVAULT-HANDOFF.md             ← this file (full instructions)
├── pepevault.html                   ← main site
├── pepevault-presskit.html          ← 10-page press kit (Save-as-PDF ready)
├── pepevault-live.html              ← live stream teaser page
├── pepevault-tweets.md              ← social media post pack
├── media/                           ← all 38 image + video assets
│   ├── pepevault-logo.svg
│   ├── hero-cover.jpg
│   ├── lineup-poster-v4.png
│   ├── hall-of-memes-cover.webp
│   ├── stampfest-3-flock-party.png
│   ├── nfc-lisbon-keyart.png
│   ├── pepex-prague-keyart.png
│   ├── live-prague-hero.png
│   ├── live-offline.png
│   ├── profile-easy-b.jpg
│   ├── hype-lisbon.mp4
│   ├── hype-prague.mp4
│   ├── reward-*.png                 (4 Counterparty reward cards)
│   ├── thanks-*.png                 (4 sponsor thank-you graphics)
│   └── spotlight-*.png              (18 artist spotlight cards)
└── v30-backup/                      ← previous version, kept for rollback safety
    ├── pepevault.v30.html
    ├── pepevault-presskit.v30.html
    ├── pepevault-tweets.v30.md
    └── PEPEVAULT-HANDOFF.v30.md
```

The HTML files are self-contained (no build step, no node_modules, no framework). Just HTML + inline CSS + inline JS + Google Fonts + image URLs.

---

## 2. ASSET URLS — TWO OPTIONS

**The HTML currently references images at `https://pub.hyperagent.com/api/published/...` URLs.** Those URLs are stable and will keep working after you deploy — **so the simplest deploy is: upload the HTML files, point the domain, ignore the `/media/` folder, ship.**

If you'd rather self-host all media (recommended for long-term portability and to remove Hyperagent's CDN from the loop):

1. Upload the contents of `/media/` to your host alongside the HTML
2. Run a global find-and-replace across the HTML files swapping every `https://pub.hyperagent.com/api/published/[id]/[filename]` URL for `/media/[filename]`
3. Test that all images, videos, and the lineup poster load

Asset categories (38 total):
- **Brand**: `pepevault-logo.svg` (used as logo + favicon + footer mark + follow-card avatar)
- **Hero**: `hero-cover.jpg` (OG image + hero background)
- **Lineup poster**: `lineup-poster-v4.png` (vivid painted festival poster with all 3 events listed)
- **Event key art**: `nfc-lisbon-keyart.png` · `pepex-prague-keyart.png` · `stampfest-3-flock-party.png`
- **Digital collectibles**: `hall-of-memes-cover.webp` (Hall of Memes Manifold mint cover by DITACRYPTO) + the PEPORACLE preview pulled from `gateway.irys.xyz` directly in the HTML
- **Sponsor thank-yous**: `thanks-fakerares.png` · `thanks-notable-pepes.png` · `thanks-northern-satoshi.png` · `thanks-stampchain.png`
- **Counterparty rewards**: `reward-vault-key.png` · `reward-ticket-stub.png` · `reward-lisboa-frog.png` · `reward-prague-frog.png`
- **Artist spotlight cards** (18): `spotlight-{artist-slug}.png` for each roster member
- **Live page**: `live-prague-hero.png` (hero) · `live-offline.png` (stream placeholder)
- **Profile pic**: `profile-easy-b.jpg` (artist Easy B's official portrait — used in his roster card)
- **Video reels**: `hype-lisbon.mp4` · `hype-prague.mp4` (8s each, 1080p)

---

## 3. DEPLOY TO PEPEVAULT.LOL — STEP BY STEP

### Step A — Register the domain
- Suggested registrars: **Cloudflare Registrar** (at-cost, integrates with Cloudflare Pages), **Porkbun** (cheapest for .lol), **Namecheap**
- Cost: ~$7–10/yr for `.lol`

### Step B — Choose a host
Pick any static host. Free tier covers this site's scale:
- **Cloudflare Pages** — recommended (best DX with Cloudflare Registrar)
- **Vercel** — drag-and-drop folder works
- **Netlify** — same pattern

### Step C — Folder structure for deploy

```
pepevault.lol/
├── index.html                       ← rename pepevault.html → index.html
├── live/
│   └── index.html                   ← rename pepevault-live.html → live/index.html
├── press/
│   └── index.html                   ← rename pepevault-presskit.html → press/index.html
└── (optional)
    ├── tweets.md                    ← pepevault-tweets.md if you want it hosted
    └── media/                       ← all assets if you self-host
        └── ... (38 files)
```

### Step D — Update internal links inside the HTML

In `pepevault.html` (main site):
- The nav "WATCH LIVE" link currently points to `https://hyperagent.com/s/kRyvMbSf9SIbp3W6jjJZOQ` — search for `kRyvMbSf9SIbp3W6jjJZOQ` and replace with `/live`
- The "Open Press Kit · Save as PDF" link points to `https://hyperagent.com/s/W98ggljH7VbD_rH-3CDmHQ` — replace with `/press`

In `pepevault-live.html`:
- The "← Back to PepeVault" and "← Main Site" links already point to `https://pepevault.lol` — change to `/` if you want them to stay on-domain

In `pepevault-presskit.html`:
- Internal link points to `https://pepevault.lol` — leave or change to `/`

(Find-and-replace in any editor — the search strings are unique enough.)

### Step E — DNS
Point `pepevault.lol` at your host. Each host's docs cover this:
- **Cloudflare Pages**: Automatic if you registered through Cloudflare Registrar
- **Vercel**: Add domain in project settings → set A record to 76.76.21.21
- **Netlify**: Same pattern, their docs are clear

### Step F — SSL
Auto-provisioned by all three hosts. No manual work needed.

---

## 4. ENABLE THE MANIFOLD MINT WIDGET (DEEP EMBED)

The main site currently uses a button labeled **▶ MINT ON MANIFOLD** that opens manifold.xyz in a new tab. To upgrade this to a deep-embed widget where visitors can connect their wallet and mint the Hall of Memes directly on pepevault.lol:

### Step 1 — Register a Manifold Developer app

1. Sign up at https://developer.manifoldxyz.dev/
2. Click **CREATE APP**
3. Fill in:
   - **App Name**: PepeVault
   - **App Description**: PepeVault digital collectible mint
   - **Redirect URI**: `https://pepevault.lol`
   - **Grant Type**: **Signature Grant**
4. Copy the generated **Client ID** — looks like a 64-char hex string

### Step 2 — Uncomment the widget assets in `<head>` of `pepevault.html`

Find the block marked `MANIFOLD DEEP-EMBED MINT WIDGET — DEPLOYER STEP-BY-STEP` near the top of the file. Below the comment block, uncomment the four lines that load Manifold's CSS and JS:

```html
<link rel="stylesheet" href="https://connect.manifoldxyz.dev/latest/connect.css">
<link rel="stylesheet" href="https://claims.manifoldxyz.dev/latest/claimComplete.css">
<script async src="https://connect.manifoldxyz.dev/latest/connect.umd.min.js"></script>
<script async src="https://claims.manifoldxyz.dev/latest/claimComplete.umd.min.js"></script>
```

### Step 3 — Uncomment the widget mount point + drop in your client_id

In the body of `pepevault.html`, search for `MANIFOLD-WIDGET-MOUNT`. You'll find a commented block with two `<div data-widget>` elements. Uncomment them and replace `TODO_REPLACE_WITH_PEPEVAULT_CLIENT_ID` with the client_id from Step 1.

### Step 4 — Optional: hide the fallback CTA

Right below the widget mount point is a fallback `<a class="collectible-cta primary-cta">▶ MINT ON MANIFOLD →</a>` link. Once the widget is working, you can either remove it or keep it as a redundancy (the widget will render the full mint UI above it).

### Reference docs
- https://docs.manifold.xyz/manifold-for-developers/guides/getting-started
- https://docs.manifold.xyz/manifold-for-developers/resources/widgets/claim-widgets

---

## 5. KNOWN LIMITATIONS / ALIGNED AFTER MIGRATION

Once on `pepevault.lol`, three things automatically improve:

1. **Social link previews:** Currently `hyperagent.com/s/...` URLs wrap with their own OG metadata, so X / Telegram / iMessage previews show "Made with Hyperagent". After migration, the proper PepeVault OG image + title + description take over (already in `<head>` of every file). The Schema.org Event JSON-LD also kicks in for SEO.
2. **Clean URLs**: `pepevault.lol` instead of `hyperagent.com/s/uvStTgkB_dHnEWifEjp3SA`.
3. **Brandability**: Bookmarks, business cards, signage all work.

---

## 6. POST-MIGRATION TODOs (NICE TO HAVE)

- **Manifold deep embed** — see Section 4 above.
- **Real Twitter timeline embed** in the FOLLOW section. Currently uses a styled "Follow @PepeVault1" card. To swap: add Twitter's widget JS (`https://platform.twitter.com/widgets.js`) and replace the `.follow-card` div with `<a class="twitter-timeline" href="https://twitter.com/pepevault1">Tweets by @pepevault1</a>`. The styled card looks better in most cases — the option's just there.
- **PEPORACLE inline embed** — Currently the "🔮 EXPERIENCE THE ORACLE" button opens the Arweave-hosted oracle in a new tab (because Hyperagent's outer sandbox lacks `allow-same-origin`, which breaks the inline doc.write trick). On `pepevault.lol` (no outer sandbox) the inline version works. To enable: in `pepevault.html` find the PEPORACLE card and swap the `<a target="_blank">` button for an iframe pointing at `https://zsepczbet4eztlmp2jyf6eonxmwtj7wr33wwdymkfrzwz5grie5a.arweave.net/zIjxZCSfCZmtj9JwXxHNuy00_tHe7WHhiixzbPTRQTo`. The inner Arweave page has auto-scaling JS that fits any viewport.
- **PEPORACLE Counterparty dispenser URL** when distribution opens. Currently the Counterparty asset link is wired to `cp20.tokenscan.io/asset/PEPORACLE`. When you have a real dispenser URL, swap that link.
- **Image optimization** — Several PNGs are 2–3MB. Compressing with tinypng / sharp / squoosh would speed up mobile load. Not blocking.
- **404 page** — Optional. Add `404.html` at the root that links back home.

---

## 7. WHAT'S WIRED + READY

The site has working:
- ✓ Mobile-responsive layout (collapsible nav, grid breakpoints at 920px / 1180px)
- ✓ Click-to-copy BTC donation address (with sandbox-safe textarea+execCommand fallback)
- ✓ OpenStreetMap iframe maps for NFC Lisbon and PEPEX Prague venues
- ✓ Real BTC donation address: `1KptKyL5e9oxwecpTFggnTtM2oFZHBq48J`
- ✓ Live ticket purchase links (NFC Summit Eventbrite + 600000000000.com)
- ✓ Mailto sponsor enquiry with pre-filled subject + body
- ✓ Clickable artist cards opening pop-out modals with smart CTA labels (pepe.wtf / stampchain.io / kaleidoscopexcp.net / fauxbitcorn.com all get correct buttons)
- ✓ Easter egg 🐸 in footer opening hidden gallery of all 18 spotlight cards
- ✓ Countdown timers on live page (auto-switches to "LIVE NOW" when dates pass)
- ✓ Press kit "Save as PDF" button (browser print-to-PDF, A4 page breaks)
- ✓ Schema.org Event markup for SEO (3 events: NFC Lisbon, Stampfest 3, PEPEX Prague)
- ✓ Open Graph + Twitter Card meta tags (will fully activate after domain migration)
- ✓ Hall of Memes Manifold drop linked (deep embed ready — see Section 4)
- ✓ PEPORACLE Counterparty card with Arweave interactive launch button
- ✓ Fake Tickets section collapsed by default (visitors expand to see lottery tiers + reward gallery)

---

## 8. CONTACT POINTS / WHO OWNS WHAT

- **X account**: @PepeVault1 (the project owns)
- **Email shown on site**: hello@pepevault.lol — needs to be set up at registrar's email forwarding or Google Workspace
- **BTC donation address**: `1KptKyL5e9oxwecpTFggnTtM2oFZHBq48J` (project's wallet)
- **Sponsorship enquiries**: mailto goes to hello@pepevault.lol (set up forwarding)
- **Hall of Memes mint**: https://manifold.xyz/@ditacrypto/id/4053440752 (creator @ditacrypto)
- **PEPORACLE asset**: https://cp20.tokenscan.io/asset/PEPORACLE (Counterparty)

---

## 9. THE 18-ARTIST ROSTER (URL CONVENTIONS)

Most artists link to pepe.wtf. Three exceptions you should know about:

| Artist | Link |
|---|---|
| DJ Pepe | `pepe.wtf/asset/DJPEPE` (it's an asset URL, since DJ Pepe is a Scrilla-created persona, not a separate artist) |
| Not Zeno | `stampchain.io/wallet/1PJ8FYDnNrtA4R3GrSesjbcbnz7iHYdKCH` (his Bitcoin Stamps wallet) |
| Faux Bitcorn | `fauxbitcorn.com` (his own site) |
| Arwyn | `kaleidoscopexcp.net/artist/Arwyn` (Kaleidoscope XCP — she co-founded Bitcoin Stamps) |

The modal CTA button on each artist card auto-detects the URL and uses the appropriate label (View Asset on pepe.wtf · View Wallet on stampchain.io · View Works on Kaleidoscope XCP · Visit fauxbitcorn.com → · etc.).

---

## 10. WHAT WAS BUILT (so you know what you're inheriting)

Across the design sessions (May 2026):
- Complete brand identity from a user-provided logo + cover image
- 30+ versions of the main site iterated through
- 10-page press kit with print-ready layout
- Live stream teaser page with dual countdown timers
- 38 illustrated brand assets across lineup poster, key art, hype reels, reward cards, sponsor graphics, spotlight cards, live-page hero, etc.
- Tweet pack covering manifesto, roster spotlights, sponsor thank-yous, countdown, lottery hook, Hall of Memes launch thread, Stampfest 3 announcement
- Two digital collectibles wired in: Hall of Memes (Ethereum/Manifold, primary) and PEPORACLE (Counterparty/Bitcoin, secondary)

Critical constraints documented (don't violate):
- Meme Conscious's real name is private (PII) — they're no longer in the roster
- Spotlight cards (18) are X teasers, NOT Counterparty assets
- Reward cards (4) ARE intended as Counterparty assets
- Sponsor names: FAKERARES (one word) is canonical
- The word "NFT" is never used in PepeVault copy — it's "digital collectible" or "digital token"
- Fake Ticket tiers are intentionally absurd / non-deliverable (folklore framing) — only the Vaultmaster tier promises real on-site artist merch

---

Real assets. Real artists. Real chaos.
DYOR · Touch grass · Trade Pepes 🐸

— PepeVault build session, May 2026
