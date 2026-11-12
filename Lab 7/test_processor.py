import calendar
import math

import pytest
from hypothesis import given, settings, strategies as st
from processor import (
    parse_season_pass_validity,
    compute_trail_gradient,
    calculate_lift_access_tier,
)

unexpected_inputs = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.booleans(),
    st.lists(st.integers()), st.dictionaries(st.text(), st.integers()),
)


@settings(report_multiple_bugs=False)
@given(unexpected_inputs)
def test_parse_season_pass_validity_no_crash(s):
    try:
        result = parse_season_pass_validity(s)
    except Exception as exc:
        pytest.fail(f"Pass validity crashed for {s!r}: {type(exc).__name__}: {exc}")
    assert isinstance(result, str)


@settings(report_multiple_bugs=False)
@given(unexpected_inputs)
def test_compute_trail_gradient_safe(s):
    try:
        result = compute_trail_gradient(s)
    except Exception as exc:
        pytest.fail(f"Gradient crashed for {s!r}: {type(exc).__name__}: {exc}")
    assert result is None or (isinstance(result, float) and math.isfinite(result) and result >= 0)


@settings(report_multiple_bugs=False)
@given(unexpected_inputs)
def test_calculate_lift_access_tier_safe(s):
    try:
        result = calculate_lift_access_tier(s)
    except Exception as exc:
        pytest.fail(f"Lift access crashed for {s!r}: {type(exc).__name__}: {exc}")
    assert result is None or result in (35.0, 60.0, 85.0, 110.0)


@given(st.dates())
def test_real_calendar_dates(expiry):
    value = f"{expiry.year:04d}/{expiry.month:02d}/{expiry.day:02d}"
    status = "VALID" if expiry.year >= 2026 else "EXPIRED"
    assert parse_season_pass_validity(value) == f"Pass Expiry: {expiry.isoformat()} ({status})"


@given(st.integers(1, 9999), st.sampled_from([2, 4, 6, 9, 11]))
def test_impossible_calendar_dates(year, month):
    day = calendar.monthrange(year, month)[1] + 1
    assert parse_season_pass_validity(f"{year:04d}/{month:02d}/{day:02d}") == "INVALID_INPUT"


@given(st.integers(0, 1_000_000), st.integers(1, 1_000_000))
def test_valid_gradients(drop, distance):
    assert compute_trail_gradient(f"{drop}:{distance}") == round(drop / distance * 100, 2)


@given(st.sampled_from(["BEG", "INT", "ADV", "ALL"]), st.booleans())
def test_known_lift_tiers(code, lowercase):
    rates = {"BEG": 35.0, "INT": 60.0, "ADV": 85.0, "ALL": 110.0}
    value = code.lower() if lowercase else code
    assert calculate_lift_access_tier(f"  {value}  ") == rates[code]


@pytest.mark.parametrize("value", ["", "1:0", "-1:10", "1:-10", "nan:1", "inf:2", "1:inf", "1:2:3", "1e308:1e-308"])
def test_invalid_gradients(value):
    assert compute_trail_gradient(value) is None


@pytest.mark.parametrize("value", ["", "2026/02/29", "2026/04/31", "0000/01/01", "2026/13/01", "2026/01/00", "2026/1/1", "2026/01/01/02"])
def test_invalid_dates(value):
    assert parse_season_pass_validity(value) == "INVALID_INPUT"


@pytest.mark.parametrize("value", ["", "XYZ", "BEGgar", "ALL-access", "123"])
def test_invalid_lift_codes(value):
    assert calculate_lift_access_tier(value) is None
