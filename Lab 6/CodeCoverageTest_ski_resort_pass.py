import pytest
from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer


def test_invalid_groups():
    with pytest.raises(ValueError, match="Invalid groups list or facility fee"):
        process_resort_bookings(None, 15)


def test_all_pass_rates_and_extras():
    groups = [
        {"is_active": False},
        {"is_active": True, "duration": "invalid"},
        {"is_active": True, "duration": "season", "skiers": [
            {"age": 11}, {"age": 65}, {"age": 30, "gear_rental": True},
            {"age": 20, "blackout_override": True}, {"age": 0}]},
        {"is_active": True, "duration": "full_day", "skiers": [{"age": 30}],
         "includes_lodge_locker": True},
        {"is_active": True, "duration": "half_day", "skiers": [
            {"age": 30}, {"age": 30, "blackout_override": True}, {"age": 30}]},
    ]
    assert process_resort_bookings(groups, 15) == {
        "total_revenue": 970.0, "status": "COMPLETED"}


def test_audit_review():
    groups = [{"is_active": True, "skiers": [{"age": -1}] * 5}]
    assert process_resort_bookings(groups, 15) == {
        "total_revenue": 0.0, "status": "AUDIT_REVIEW"}


def test_zero_sales():
    assert process_resort_bookings([], 15) == {
        "total_revenue": 0.0, "status": "ZERO_SALES"}


@pytest.mark.parametrize("streams, expected", [
    ([], "NO_DATA"),
    ([[20, 46, 45, 47]], "SAFE_OPERATION"),
    ([[46, 47]], "SUSPEND_LIFT"),
])
def test_wind_status(streams, expected):
    assert check_chairlift_anemometer(streams) == expected
