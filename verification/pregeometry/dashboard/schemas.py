"""Strict telemetry schemas for the UIDT PR-0.5 dashboard.

The dashboard is an observer layer only. These schemas validate telemetry
records after PR-0 has produced them; they do not define growth dynamics.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Iterable, Literal

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, StrictBool, field_validator, model_validator


TELEMETRY_SCHEMA_VERSION = "pr0.telemetry.v1"
SUMMARY_SCHEMA_VERSION = "pr0.telemetry.summary.v1"
RUN_ID_PATTERN = r"^[A-Za-z0-9_.-]+$"

FORBIDDEN_VISUALIZATION_LABELS = (
    "Big Bang",
    "universe simulation",
    "spacetime emergence",
    "cosmological evolution",
    "FLRW",
    "de Sitter",
    "Minkowski",
    "3+1",
    "G_SM",
    "Standard Model emergence",
)


def assert_no_forbidden_visualization_text(texts: str | Iterable[str]) -> None:
    """Fail fast if dashboard-visible text uses forbidden interpretation labels."""
    if isinstance(texts, str):
        candidates = (texts,)
    else:
        candidates = tuple(texts)
    for text in candidates:
        lowered = text.lower()
        for label in FORBIDDEN_VISUALIZATION_LABELS:
            if label.lower() in lowered:
                raise ValueError(f"Forbidden visualization/claim label found: {label!r}")


class StrictTelemetryModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class InvariantBlock(StrictTelemetryModel):
    N: NonNegativeInt
    E: NonNegativeInt
    C: NonNegativeInt
    beta_1: NonNegativeInt

    @model_validator(mode="after")
    def validate_beta_1_formula(self) -> "InvariantBlock":
        expected = self.E - self.N + self.C
        if expected < 0 or self.beta_1 != expected:
            raise ValueError("beta_1 must equal E - N + C exactly.")
        return self


class NullModelRow(StrictTelemetryModel):
    name: str
    invariants: InvariantBlock
    claim_status: Literal["[D/E]"] = "[D/E]"

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        assert_no_forbidden_visualization_text(value)
        return value


class TelemetryEvent(StrictTelemetryModel):
    schema_version: Literal["pr0.telemetry.v1"] = TELEMETRY_SCHEMA_VERSION
    run_id: str = Field(pattern=RUN_ID_PATTERN)
    tick: NonNegativeInt
    seed: int
    model: str
    rule: str
    N: NonNegativeInt
    E: NonNegativeInt
    C: NonNegativeInt
    beta_1: NonNegativeInt
    acyclic: StrictBool
    leakage_passed: StrictBool
    invariant_passed: StrictBool
    claim_status: Literal["[D/E]"] = "[D/E]"
    timestamp_utc: datetime

    @field_validator("run_id")
    @classmethod
    def validate_run_id(cls, value: str) -> str:
        if not re.fullmatch(RUN_ID_PATTERN, value):
            raise ValueError("run_id must be filename-safe.")
        return value

    @field_validator("model", "rule")
    @classmethod
    def validate_dashboard_text(cls, value: str) -> str:
        assert_no_forbidden_visualization_text(value)
        return value

    @field_validator("timestamp_utc")
    @classmethod
    def validate_utc_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("timestamp_utc must be timezone-aware.")
        as_utc = value.astimezone(timezone.utc)
        if as_utc.utcoffset() != timezone.utc.utcoffset(as_utc):
            raise ValueError("timestamp_utc must be convertible to UTC.")
        return as_utc

    @model_validator(mode="after")
    def validate_invariants(self) -> "TelemetryEvent":
        InvariantBlock(N=self.N, E=self.E, C=self.C, beta_1=self.beta_1)
        if not self.acyclic:
            raise ValueError("PR-0.5 telemetry requires DAG-safe events to remain acyclic.")
        if not self.leakage_passed or not self.invariant_passed:
            raise ValueError("Dashboard telemetry only records successful PR-0 invariant events.")
        return self

    def invariants(self) -> InvariantBlock:
        return InvariantBlock(N=self.N, E=self.E, C=self.C, beta_1=self.beta_1)


class RunSummary(StrictTelemetryModel):
    schema_version: Literal["pr0.telemetry.summary.v1"] = SUMMARY_SCHEMA_VERSION
    run_id: str = Field(pattern=RUN_ID_PATTERN)
    seed: int
    iterations: NonNegativeInt
    null_model: str
    event_count: NonNegativeInt
    latest_event: TelemetryEvent | None
    uidt_invariants: InvariantBlock
    null_model_row: NullModelRow
    leakage_passed: StrictBool
    invariant_passed: StrictBool
    claim_status: Literal["[D/E]"] = "[D/E]"
    run_json: str
    report: str

    @field_validator("run_id")
    @classmethod
    def validate_run_id(cls, value: str) -> str:
        if not re.fullmatch(RUN_ID_PATTERN, value):
            raise ValueError("run_id must be filename-safe.")
        return value

    @field_validator("null_model", "run_json", "report")
    @classmethod
    def validate_text(cls, value: str) -> str:
        assert_no_forbidden_visualization_text(value)
        return value

