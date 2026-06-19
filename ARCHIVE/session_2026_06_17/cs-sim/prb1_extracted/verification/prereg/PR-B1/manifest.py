"""
Data Integrity Manifest
========================
SHA-256 manifest generation and verification for the data-freeze protocol.
Ensures that raw simulation data is cryptographically sealed before AG-Eval
is permitted to ingest it.

Usage:
    # Generate manifest after AG-Sim completes:
    python -m verification.prereg.PR-B1.manifest generate

    # Verify manifest integrity:
    python -m verification.prereg.PR-B1.manifest verify
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone
from typing import Any

from .config import RAW_DATA_DIR, MANIFEST_DIR


def _sha256_file(filepath: pathlib.Path) -> str:
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def generate_manifest(
    raw_dir: pathlib.Path | None = None,
    manifest_dir: pathlib.Path | None = None,
) -> dict[str, Any]:
    """Generate a SHA-256 manifest of all files in the raw data directory.

    Parameters
    ----------
    raw_dir : Path, optional
        Directory containing raw simulation data.
    manifest_dir : Path, optional
        Directory to write the manifest JSON.

    Returns
    -------
    dict
        The manifest dictionary.
    """
    if raw_dir is None:
        raw_dir = RAW_DATA_DIR
    if manifest_dir is None:
        manifest_dir = MANIFEST_DIR

    if not raw_dir.is_dir():
        raise FileNotFoundError(
            f"Raw data directory not found: {raw_dir}. "
            "AG-Sim must complete before manifest generation."
        )

    manifest: dict[str, Any] = {
        "protocol_id": "PREREG-PR-B1-002-AG2",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "raw_data_root": str(raw_dir),
        "file_count": 0,
        "total_bytes": 0,
        "files": {},
    }

    all_files = sorted(raw_dir.rglob("*"))
    for fpath in all_files:
        if fpath.is_file() and fpath.name != ".gitkeep":
            rel = fpath.relative_to(raw_dir).as_posix()
            size = fpath.stat().st_size
            digest = _sha256_file(fpath)
            manifest["files"][rel] = {
                "sha256": digest,
                "size_bytes": size,
            }
            manifest["file_count"] += 1
            manifest["total_bytes"] += size

    # Compute manifest-level hash (hash of all individual hashes, sorted)
    all_hashes = sorted(manifest["files"][k]["sha256"] for k in manifest["files"])
    meta_hash = hashlib.sha256(
        "\n".join(all_hashes).encode()
    ).hexdigest()
    manifest["manifest_hash"] = meta_hash

    # Write manifest
    manifest_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    manifest_path = manifest_dir / f"data-freeze-manifest-{timestamp}.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[MANIFEST] Generated: {manifest_path}")
    print(f"[MANIFEST] Files: {manifest['file_count']}")
    print(f"[MANIFEST] Total bytes: {manifest['total_bytes']:,}")
    print(f"[MANIFEST] Manifest hash: {meta_hash}")

    return manifest


def verify_manifest(
    manifest_path: pathlib.Path,
    raw_dir: pathlib.Path | None = None,
) -> tuple[bool, list[str]]:
    """Verify raw data against a previously generated manifest.

    Parameters
    ----------
    manifest_path : Path
        Path to the manifest JSON file.
    raw_dir : Path, optional
        Raw data directory.  Defaults to the path stored in the manifest.

    Returns
    -------
    (passed, discrepancies) : (bool, list[str])
    """
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    if raw_dir is None:
        raw_dir = pathlib.Path(manifest["raw_data_root"])

    discrepancies: list[str] = []

    # Check each file in manifest
    for rel_path, expected in manifest["files"].items():
        fpath = raw_dir / rel_path
        if not fpath.is_file():
            discrepancies.append(f"MISSING: {rel_path}")
            continue

        actual_hash = _sha256_file(fpath)
        if actual_hash != expected["sha256"]:
            discrepancies.append(
                f"HASH MISMATCH: {rel_path} "
                f"(expected {expected['sha256'][:16]}..., "
                f"got {actual_hash[:16]}...)"
            )

        actual_size = fpath.stat().st_size
        if actual_size != expected["size_bytes"]:
            discrepancies.append(
                f"SIZE MISMATCH: {rel_path} "
                f"(expected {expected['size_bytes']}, got {actual_size})"
            )

    # Check for files present on disk but not in manifest
    for fpath in sorted(raw_dir.rglob("*")):
        if fpath.is_file() and fpath.name != ".gitkeep":
            rel = fpath.relative_to(raw_dir).as_posix()
            if rel not in manifest["files"]:
                discrepancies.append(f"EXTRA FILE (post-freeze?): {rel}")

    if discrepancies:
        print("[MANIFEST] *** VERIFICATION FAILED ***")
        for d in discrepancies:
            print(f"  {d}")
        return False, discrepancies
    else:
        print("[MANIFEST] Verification passed. Data integrity confirmed.")
        return True, []


def get_latest_manifest(
    manifest_dir: pathlib.Path | None = None,
) -> pathlib.Path | None:
    """Return the path to the most recent manifest file, or None."""
    if manifest_dir is None:
        manifest_dir = MANIFEST_DIR
    if not manifest_dir.is_dir():
        return None
    manifests = sorted(manifest_dir.glob("data-freeze-manifest-*.json"))
    return manifests[-1] if manifests else None


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m verification.prereg.PR-B1.manifest [generate|verify]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "generate":
        generate_manifest()
    elif cmd == "verify":
        manifest_path = get_latest_manifest()
        if manifest_path is None:
            print("[MANIFEST] No manifest found. Run 'generate' first.")
            sys.exit(1)
        passed, _ = verify_manifest(manifest_path)
        sys.exit(0 if passed else 1)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
