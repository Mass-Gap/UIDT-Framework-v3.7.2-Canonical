"""Fail-fast target-leakage audit for PR-0 generation files.

The default audit scope is deliberately narrow. It scans generation code and
configuration files, not documentation, because documentation may need to name
forbidden target patterns while explaining why they are disallowed.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


FORBIDDEN_TOKENS: Tuple[str, ...] = (
    "Minkowski",
    "eta_mu_nu",
    "Lorentz",
    "FLRW",
    "deSitter",
    "3+1",
    "SU(3)",
    "SU(2)",
    "U(1)",
    "G_SM",
    "gamma=16.339",
    "Planck18",
    "LambdaCDM target",
    "H0 target",
    "S8 target",
)


@dataclass(frozen=True)
class LeakageHit:
    path: str
    token: str
    line_number: int
    line_excerpt: str

    def as_jsonable(self) -> dict:
        return {
            "path": self.path,
            "token": self.token,
            "line_number": self.line_number,
            "line_excerpt": self.line_excerpt,
        }


@dataclass(frozen=True)
class LeakageAuditResult:
    scanned_paths: Tuple[str, ...]
    hits: Tuple[LeakageHit, ...]

    @property
    def passed(self) -> bool:
        return not self.hits

    def as_jsonable(self) -> dict:
        return {
            "passed": self.passed,
            "scanned_paths": list(self.scanned_paths),
            "hits": [hit.as_jsonable() for hit in self.hits],
        }


class LeakageAuditError(RuntimeError):
    """Raised when target-leakage tokens are found."""


def default_generation_paths(project_root: Path) -> Tuple[Path, ...]:
    """Return default files/directories scanned by PR-0 leakage audit."""
    root = Path(project_root)
    candidates = [
        root / "verification" / "pregeometry" / "growth_rules.py",
        root / "verification" / "pregeometry" / "configs",
    ]
    return tuple(path for path in candidates if path.exists())


def audit_paths(paths: Iterable[Path], *, project_root: Path | None = None) -> LeakageAuditResult:
    """Scan paths and return a structured leakage-audit result."""
    root = Path(project_root).resolve() if project_root is not None else None
    expanded = tuple(_iter_scannable_files(paths))
    hits: List[LeakageHit] = []
    scanned_paths = []

    for path in expanded:
        path = path.resolve()
        scanned_paths.append(_display_path(path, root))
        text = path.read_text(encoding="utf-8")
        hits.extend(_scan_text(path, text, root=root))

    return LeakageAuditResult(scanned_paths=tuple(scanned_paths), hits=tuple(hits))


def assert_no_leakage(paths: Iterable[Path], *, project_root: Path | None = None) -> LeakageAuditResult:
    """Raise LeakageAuditError if the given paths contain forbidden tokens."""
    result = audit_paths(paths, project_root=project_root)
    if not result.passed:
        formatted = "\n".join(
            f"{hit.path}:{hit.line_number}: forbidden token {hit.token!r}: {hit.line_excerpt}"
            for hit in result.hits
        )
        raise LeakageAuditError(f"Target-leakage audit failed:\n{formatted}")
    return result


def _iter_scannable_files(paths: Iterable[Path]) -> Iterable[Path]:
    for item in paths:
        path = Path(item)
        if not path.exists():
            continue
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and child.suffix in {".py", ".json", ".yaml", ".yml", ".toml", ".txt"}:
                    yield child
        elif path.is_file():
            yield path


def _scan_text(path: Path, text: str, *, root: Path | None = None) -> Tuple[LeakageHit, ...]:
    hits: List[LeakageHit] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for token in FORBIDDEN_TOKENS:
            if token in line:
                hits.append(
                    LeakageHit(
                        path=_display_path(path, root),
                        token=token,
                        line_number=line_number,
                        line_excerpt=line.strip(),
                    )
                )
    return tuple(hits)


def _display_path(path: Path, root: Path | None) -> str:
    if root is None:
        return str(path)
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)
