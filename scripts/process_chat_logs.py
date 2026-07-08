#!/usr/bin/env python3
"""
UIDT Framework v4.0 — Privacy-Safe Chat Log Chunker
====================================================
[E] — Diagnostic software artifact. No physical claims.

Parses raw chat / markdown / JSON log files from a private workspace,
strips all private markers, and writes stable, reviewable semantic
chunks to `.uidt-local/chunks/` (NEVER to the public git tree).

Privacy guarantees:
  - Local paths, usernames, tokens, session IDs are redacted.
  - `.uidt-local` references are masked.
  - Machine-specific metadata is stripped.
  - Output MUST land in `.uidt-local/` (.gitignore enforced).
  - Nothing is automatically promoted to ontology or public status.

Usage:
  python scripts/process_chat_logs.py [--input-dir DIR] [--output-dir DIR]
                                      [--max-chunk-size N] [--format jsonl|json]

Defaults:
  --input-dir    raw_chat_logs/
  --output-dir   .uidt-local/chunks/
  --max-chunk-size 2000   (characters per chunk)
  --format       jsonl
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ============================================================================
# PRIVACY REDACTION RULES
# ============================================================================

# Patterns that MUST be redacted from all output
REDACTION_PATTERNS = [
    # Windows-style absolute paths
    (re.compile(r'[A-Z]:\\(?:Users|Benutzer)\\[^\s\\]+', re.IGNORECASE),
     '[REDACTED_LOCAL_PATH]'),
    # Unix-style home paths
    (re.compile(r'/(?:home|Users)/[^\s/]+', re.IGNORECASE),
     '[REDACTED_LOCAL_PATH]'),
    # .uidt-local references
    (re.compile(r'\.uidt-local[^\s]*'),
     '[REDACTED_LOCAL_REF]'),
    # Generic tokens / API keys (hex strings > 20 chars)
    (re.compile(r'(?:token|key|secret|password|auth)[=:]\s*["\']?[A-Za-z0-9_\-]{20,}["\']?',
                re.IGNORECASE),
     '[REDACTED_CREDENTIAL]'),
    # Session IDs (UUID-like)
    (re.compile(r'(?:session[_-]?id|sid)[=:]\s*["\']?[0-9a-f\-]{32,}["\']?',
                re.IGNORECASE),
     '[REDACTED_SESSION_ID]'),
    # Email addresses
    (re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'),
     '[REDACTED_EMAIL]'),
    # AWS tokens in URLs
    (re.compile(r'AWSAccessKeyId=[^\s&]+'),
     'AWSAccessKeyId=[REDACTED]'),
    (re.compile(r'x-amz-security-token=[^\s&]+'),
     'x-amz-security-token=[REDACTED]'),
    (re.compile(r'Signature=[^\s&]+'),
     'Signature=[REDACTED]'),
]


def redact(text: str) -> str:
    """Apply all privacy redaction rules to a text string."""
    for pattern, replacement in REDACTION_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


# ============================================================================
# CHUNKING ENGINE
# ============================================================================

# Markdown heading pattern for semantic splitting
HEADING_RE = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)


def chunk_id(source_file: str, index: int, content: str) -> str:
    """Generate a deterministic chunk ID from source and content hash."""
    h = hashlib.sha256(content.encode('utf-8')).hexdigest()[:12]
    return f"{Path(source_file).stem}_{index:04d}_{h}"


def split_by_headings(text: str, max_size: int) -> list:
    """Split text into semantic chunks at markdown headings.

    Falls back to hard-split at max_size if a section is too large.
    Returns list of dicts with 'section_title' and 'content' keys.
    """
    chunks = []
    positions = [(m.start(), m.group(2).strip()) for m in HEADING_RE.finditer(text)]

    if not positions:
        # No headings: split by paragraph or hard-split
        return _hard_split(text, max_size, section_title="(no heading)")

    # Add implicit start if text begins before first heading
    if positions[0][0] > 0:
        preamble = text[:positions[0][0]].strip()
        if preamble:
            chunks.extend(_hard_split(preamble, max_size, section_title="(preamble)"))

    for i, (pos, title) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        section_content = text[pos:end].strip()
        if len(section_content) <= max_size:
            chunks.append({"section_title": title, "content": section_content})
        else:
            chunks.extend(_hard_split(section_content, max_size, section_title=title))

    return chunks


def _hard_split(text: str, max_size: int, section_title: str) -> list:
    """Split text into fixed-size chunks, preferring paragraph boundaries."""
    result = []
    paragraphs = text.split('\n\n')
    current = ""

    for para in paragraphs:
        candidate = (current + "\n\n" + para).strip() if current else para.strip()
        if len(candidate) <= max_size:
            current = candidate
        else:
            if current:
                result.append({"section_title": section_title, "content": current})
            # If single paragraph exceeds max_size, split at max_size
            while len(para) > max_size:
                result.append({"section_title": section_title, "content": para[:max_size]})
                para = para[max_size:]
            current = para.strip()

    if current:
        result.append({"section_title": section_title, "content": current})

    return result


# ============================================================================
# CLAIM CLASS HEURISTICS
# ============================================================================

CLAIM_KEYWORDS = {
    'A':  [r'\bproven\b', r'\bexact\b', r'\bidentity\b', r'residual.*<.*10'],
    'B':  [r'\blattice\b', r'\bQCD\b', r'\bconsistent\b'],
    'C':  [r'\bcalibrat', r'\bDESI\b', r'\bJWST\b', r'\bACT\b', r'\bphenomenolog'],
    'D':  [r'\bpredict', r'\bunconfirm', r'\bpropos'],
    'E':  [r'\bspeculat', r'\bwithdraw', r'\bretract'],
}


def guess_claim_class(text: str) -> str:
    """Heuristic guess for evidence class. Always needs_human_review."""
    text_lower = text.lower()
    for cls in ['A', 'B', 'C', 'D', 'E']:
        for kw in CLAIM_KEYWORDS[cls]:
            if re.search(kw, text_lower):
                return cls
    return 'E'  # Default: speculative / unclassified


def contains_private(text: str) -> bool:
    """Check if the original (pre-redaction) text contains private material."""
    for pattern, _ in REDACTION_PATTERNS:
        if pattern.search(text):
            return True
    return False


# ============================================================================
# FILE LOADERS
# ============================================================================

def load_file(filepath: Path) -> str:
    """Load a file as text. Supports .json (extracts content fields), .md, .txt."""
    raw = filepath.read_text(encoding='utf-8', errors='replace')

    if filepath.suffix == '.json':
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                # Assume list of message objects
                parts = []
                for item in data:
                    if isinstance(item, dict):
                        content = item.get('content', item.get('text', ''))
                        role = item.get('role', 'unknown')
                        parts.append(f"## [{role}]\n{content}")
                    else:
                        parts.append(str(item))
                return '\n\n'.join(parts)
            elif isinstance(data, dict):
                return json.dumps(data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            pass  # Fall through to raw text

    return raw


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def process_directory(input_dir: Path, output_dir: Path,
                      max_chunk_size: int, output_format: str) -> int:
    """Process all files in input_dir and write chunks to output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)

    supported = {'.md', '.txt', '.json', '.jsonl', '.log'}
    files = sorted(f for f in input_dir.rglob('*') if f.is_file() and f.suffix in supported)

    if not files:
        print(f"WARNING: No supported files found in {input_dir}", file=sys.stderr)
        return 0

    all_chunks = []
    global_index = 0

    for filepath in files:
        print(f"Processing: {filepath.name}")
        raw_text = load_file(filepath)
        has_private = contains_private(raw_text)
        clean_text = redact(raw_text)

        sections = split_by_headings(clean_text, max_chunk_size)

        for section in sections:
            cid = chunk_id(str(filepath), global_index, section['content'])
            chunk_record = {
                "chunk_id": cid,
                "source_file": filepath.name,
                "section_title": section['section_title'],
                "content": section['content'],
                "claim_class_candidate": guess_claim_class(section['content']),
                "needs_human_review": True,
                "contains_private_material": has_private,
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "char_count": len(section['content']),
            }
            all_chunks.append(chunk_record)
            global_index += 1

    # Write output
    if output_format == 'jsonl':
        out_path = output_dir / "chunks.jsonl"
        with open(out_path, 'w', encoding='utf-8') as f:
            for chunk in all_chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
    else:
        out_path = output_dir / "chunks.json"
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {len(all_chunks)} chunks to {out_path}")
    print(f"  Files processed: {len(files)}")
    print(f"  Chunks with private material: "
          f"{sum(1 for c in all_chunks if c['contains_private_material'])}")
    print(f"  All chunks flagged needs_human_review=True (enforced)")

    return len(all_chunks)


def main():
    parser = argparse.ArgumentParser(
        description="UIDT Privacy-Safe Chat Log Chunker (Phase 8)")
    parser.add_argument('--input-dir', type=Path, default=Path('raw_chat_logs'),
                        help='Directory containing raw chat/log files')
    parser.add_argument('--output-dir', type=Path, default=Path('.uidt-local/chunks'),
                        help='Output directory (MUST be in .uidt-local/)')
    parser.add_argument('--max-chunk-size', type=int, default=2000,
                        help='Maximum characters per chunk')
    parser.add_argument('--format', choices=['jsonl', 'json'], default='jsonl',
                        help='Output format')
    args = parser.parse_args()

    # SAFETY: enforce output stays in .uidt-local
    output_str = str(args.output_dir.resolve())
    if '.uidt-local' not in output_str:
        print("FATAL: Output directory MUST be inside .uidt-local/ to prevent "
              "private data from entering the public git tree.", file=sys.stderr)
        sys.exit(1)

    if not args.input_dir.exists():
        print(f"FATAL: Input directory '{args.input_dir}' does not exist.",
              file=sys.stderr)
        sys.exit(1)

    process_directory(args.input_dir, args.output_dir,
                      args.max_chunk_size, args.format)


if __name__ == '__main__':
    main()
