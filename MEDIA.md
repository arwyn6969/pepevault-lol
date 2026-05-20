# Updating media on pepevault.lol

The 38+ media assets the site references are NOT stored in this Git repo — they
live in Cloudflare R2 at `https://media.pepevault.lol/<filename>`. When you add
new artwork, video reels, sponsor graphics, or replacement images, push them
directly to R2 using the boto3 helper script below.

## One-time setup

Required: Python 3.9+ and the `boto3` package.

```bash
pip install boto3
```

Set four environment variables (or write them into a `.env` and source it):

```bash
export R2_ACCESS_KEY_ID=<provided separately — do not commit>
export R2_SECRET_ACCESS_KEY=<provided separately — do not commit>
export R2_ENDPOINT_URL="https://1fad7381eebca78dd4db41c7af2f595d.r2.cloudflarestorage.com"
export R2_BUCKET="pepevault-media"
```

The Access Key ID + Secret will be sent to you out-of-band. Treat them as
secrets — anyone with these can write to the R2 bucket. Never commit them.

## Day-to-day upload

```bash
# Upload one file
python scripts/upload_to_r2.py optimized/spotlight-new-artist.webp

# Upload everything in a folder (recursive, flat keys)
python scripts/upload_to_r2.py optimized/

# Dry-run first if you're unsure
python scripts/upload_to_r2.py --dry-run optimized/
```

The script sets the right `Content-Type` per extension and applies a
1-year immutable `Cache-Control` (`public, max-age=31536000, immutable`).
Files become live at `https://media.pepevault.lol/<filename>` immediately.

## Filename conventions (IMPORTANT)

R2 caches aggressively. **If you upload a file with the same name as one already
in the bucket, browsers and CDN edges may serve the old version for up to a
year.** Two ways to handle replacements:

- **Preferred — version the filename**: `lineup-poster-v4.webp` → `lineup-poster-v5.webp`,
  then update the URL reference in `index.html` to match. The repo's existing
  `v30-backup/` pattern shows this convention.
- **Otherwise — purge the cache** after re-upload: ask the site owner to run
  `npx wrangler r2 object delete pepevault-media/<filename>` followed by a
  fresh upload; that forces edges to re-fetch.

## Optimization (recommended)

Source PNGs from design tools are typically 2-4 MB each. The current asset set
was converted to WebP at quality 85 (PNGs) and 82 (JPGs), achieving ~85% size
reduction with no visible quality loss. To match that conversion:

```bash
# install once
sudo apt install webp
# convert
cwebp -q 85 source.png -o optimized.webp
cwebp -q 82 source.jpg -o optimized.webp
```

SVG: run through `svgo` (npm) for a free ~30-40% size cut.

Keep MP4 video reels as-is — re-encoding hurts more than it helps at this scale.

## File-type policy

| Type | Extension | Cache | Notes |
|---|---|---|---|
| Photos / artwork rasters | `.webp` | 1yr immutable | Convert from PNG/JPG with cwebp |
| Logos / icons | `.svg` | 1yr immutable | Run `svgo` to shrink |
| Video reels | `.mp4` | 1yr immutable | H.264, ≤1080p, `preload="metadata"` set in HTML |
| Posters / cover art | `.webp` | 1yr immutable | If transparency required, lossless WebP |

## Verifying the upload

After running the script, the success line includes the live URL:

```
  OK   spotlight-new-artist.webp  ( 412.3 KB, image/webp)  -> https://media.pepevault.lol/spotlight-new-artist.webp
```

Sanity-check by curl-ing the URL:

```bash
curl -I https://media.pepevault.lol/<filename>
# Should return: HTTP/2 200, content-type matches, cache-control: public, max-age=31536000, immutable
```

If the file appears in `index.html` already (referenced by URL), CF will pick
it up on the next request. If it's a NEW file, you also need to add the `<img
src="...">` or `<source src="...">` reference in `index.html` and push that
through GitHub for the site to actually use it.

## Where credentials come from

The R2 Access Key ID + Secret are generated in the Cloudflare R2 dashboard
under "Manage R2 API Tokens" → "Create API Token". They're scoped specifically
to the `pepevault-media` bucket with read+write permission. The site owner
manages issuance and rotation.

If your token stops working, ping the site owner — they can issue a fresh one
in 30 seconds.
