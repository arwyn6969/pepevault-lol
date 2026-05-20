#!/usr/bin/env python3
"""
Upload files to the pepevault-media R2 bucket via S3-compatible API.

Usage:
    # Single file
    python upload_to_r2.py media/spotlight-new-artist.webp

    # Directory (recursive — uploads every file beneath)
    python upload_to_r2.py optimized/

    # Multiple paths
    python upload_to_r2.py media/foo.webp media/bar.svg

    # Dry-run (show what would upload, don't transfer)
    python upload_to_r2.py --dry-run optimized/

Required env vars (set in shell or .env before running):
    R2_ACCESS_KEY_ID       — from Cloudflare R2 → Manage R2 API Tokens
    R2_SECRET_ACCESS_KEY   — same; shown only once at token creation
    R2_ENDPOINT_URL        — https://1fad7381eebca78dd4db41c7af2f595d.r2.cloudflarestorage.com
    R2_BUCKET              — pepevault-media

Files are uploaded with:
    - Cache-Control: public, max-age=31536000, immutable
    - Content-Type: auto-detected by extension
    - Key (R2 path) = basename of local file (flat — no subdirectory nesting)

Live CDN URL after upload: https://media.pepevault.lol/<filename>

Install: pip install boto3
"""

import argparse
import mimetypes
import os
import sys
from pathlib import Path

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    print("ERROR: boto3 not installed. Run: pip install boto3", file=sys.stderr)
    sys.exit(2)

# Per-extension content-type overrides (mimetypes module sometimes returns weak defaults)
CONTENT_TYPE_OVERRIDES = {
    ".webp": "image/webp",
    ".avif": "image/avif",
    ".svg": "image/svg+xml",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".json": "application/json",
    ".txt": "text/plain; charset=utf-8",
}

CACHE_CONTROL = "public, max-age=31536000, immutable"


def content_type_for(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in CONTENT_TYPE_OVERRIDES:
        return CONTENT_TYPE_OVERRIDES[ext]
    guess, _ = mimetypes.guess_type(str(path))
    return guess or "application/octet-stream"


def collect_files(targets: list[str]) -> list[Path]:
    files = []
    for t in targets:
        p = Path(t).resolve()
        if not p.exists():
            print(f"WARN: not found, skipping: {p}", file=sys.stderr)
            continue
        if p.is_dir():
            for sub in sorted(p.rglob("*")):
                if sub.is_file() and not sub.name.startswith("."):
                    files.append(sub)
        else:
            files.append(p)
    return files


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="Files and/or directories to upload")
    ap.add_argument("--dry-run", action="store_true", help="Print what would happen, don't upload")
    ap.add_argument("--prefix", default="", help="Optional key prefix (e.g. 'v2/' to namespace uploads)")
    args = ap.parse_args()

    required = ["R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_ENDPOINT_URL", "R2_BUCKET"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"ERROR: missing env vars: {', '.join(missing)}", file=sys.stderr)
        print("See script header for setup instructions.", file=sys.stderr)
        sys.exit(2)

    bucket = os.environ["R2_BUCKET"]
    endpoint = os.environ["R2_ENDPOINT_URL"]

    files = collect_files(args.paths)
    if not files:
        print("No files to upload.", file=sys.stderr)
        sys.exit(1)

    print(f"R2 endpoint: {endpoint}")
    print(f"R2 bucket:   {bucket}")
    print(f"Files:       {len(files)}")
    print()

    if args.dry_run:
        for f in files:
            ct = content_type_for(f)
            key = args.prefix + f.name
            print(f"  [DRY-RUN] {f.name:50s}  ({ct})  -> {bucket}/{key}")
        print(f"\nDry-run complete. {len(files)} file(s) would have been uploaded.")
        return

    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",  # R2 ignores region but boto3 requires the kwarg
    )

    ok = 0
    failed = 0
    for f in files:
        ct = content_type_for(f)
        key = args.prefix + f.name
        size_kb = f.stat().st_size / 1024
        try:
            s3.upload_file(
                Filename=str(f),
                Bucket=bucket,
                Key=key,
                ExtraArgs={"ContentType": ct, "CacheControl": CACHE_CONTROL},
            )
            ok += 1
            print(f"  OK   {f.name:50s}  ({size_kb:7.1f} KB, {ct})  -> https://media.pepevault.lol/{key}")
        except ClientError as e:
            failed += 1
            print(f"  FAIL {f.name}: {e}", file=sys.stderr)

    print(f"\nDone. {ok} uploaded, {failed} failed.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
