"""Small deterministic statistics helpers for PR-1 software metrics."""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import Sequence


def mean_fraction(values: Sequence[int | Fraction]) -> Fraction:
    if not values:
        return Fraction(0, 1)
    return sum((Fraction(value) for value in values), Fraction(0, 1)) / len(values)


def permutation_p_value(observed_distance: int | Fraction, null_distances: Sequence[int | Fraction]) -> Fraction:
    """Return a conservative right-tail permutation p-value as an exact fraction."""
    observed = Fraction(observed_distance)
    nulls = tuple(Fraction(value) for value in null_distances)
    if not nulls:
        return Fraction(1, 1)
    extreme_count = sum(1 for value in nulls if value >= observed)
    return Fraction(extreme_count + 1, len(nulls) + 1)


def bootstrap_confidence_interval(
    values: Sequence[int | Fraction],
    *,
    seed: int,
    samples: int = 128,
) -> tuple[Fraction, Fraction]:
    """Return a deterministic percentile interval for the sample mean."""
    fractions = tuple(Fraction(value) for value in values)
    if not fractions:
        return (Fraction(0, 1), Fraction(0, 1))
    if samples <= 0:
        raise ValueError("samples must be positive.")

    rng = Random(seed)
    means = []
    for _ in range(samples):
        draw = [fractions[rng.randrange(len(fractions))] for _ in fractions]
        means.append(mean_fraction(draw))
    means.sort()
    low_index = (samples * 5) // 100
    high_index = min(samples - 1, (samples * 95) // 100)
    return (means[low_index], means[high_index])


def fraction_to_jsonable(value: Fraction) -> dict[str, int | str]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": _decimal_string(value),
    }


def _decimal_string(value: Fraction) -> str:
    sign = "-" if value < 0 else ""
    value = abs(value)
    whole = value.numerator // value.denominator
    remainder = value.numerator % value.denominator
    if remainder == 0:
        return f"{sign}{whole}"
    digits = []
    for _ in range(12):
        remainder *= 10
        digits.append(str(remainder // value.denominator))
        remainder %= value.denominator
        if remainder == 0:
            break
    return f"{sign}{whole}.{''.join(digits)}"

