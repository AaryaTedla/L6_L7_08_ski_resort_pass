import math
import re
from datetime import date


def parse_season_pass_validity(date_str):
    """Return the expiry status, or INVALID_INPUT for malformed/invalid dates."""
    if not isinstance(date_str, str):
        return "INVALID_INPUT"
    value = date_str.strip()
    if re.fullmatch(r"[0-9]{4}/[0-9]{2}/[0-9]{2}", value) is None:
        return "INVALID_INPUT"
    try:
        year, month, day = map(int, value.split('/'))
        expiry = date(year, month, day)
    except ValueError:
        return "INVALID_INPUT"
    # Preserve the assignment's original validity rule: year >= 2026.
    status = "VALID" if year >= 2026 else "EXPIRED"
    return f"Pass Expiry: {expiry.isoformat()} ({status})"


def compute_trail_gradient(elevation_str):
    """Return a finite gradient, or None for invalid measurements."""
    if not isinstance(elevation_str, str):
        return None
    parts = elevation_str.split(':')
    if len(parts) != 2:
        return None
    try:
        drop, distance = map(float, parts)
    except (ValueError, OverflowError):
        return None
    if not (math.isfinite(drop) and math.isfinite(distance)):
        return None
    if drop < 0 or distance <= 0:
        return None
    gradient_pct = (drop / distance) * 100.0
    if not math.isfinite(gradient_pct):
        return None
    return round(gradient_pct, 2)


def calculate_lift_access_tier(zone_code):
    """Return the price for an exact zone code, or None if invalid."""
    if not isinstance(zone_code, str):
        return None
    zone_rates = {"BEG": 35.0, "INT": 60.0, "ADV": 85.0, "ALL": 110.0}
    return zone_rates.get(zone_code.strip().upper())


def main():
    print("==== Running parse_season_pass_validity ====")
    d_input = input("Enter pass expiry (YYYY/MM/DD): ")
    print(parse_season_pass_validity(d_input))

    print("\n==== Running compute_trail_gradient ====")
    e_input = input("Enter drop:distance (e.g. 250:1000): ")
    gradient = compute_trail_gradient(e_input)
    print("Gradient %:", gradient if gradient is not None else "INVALID_INPUT")

    print("\n==== Running calculate_lift_access_tier ====")
    z_input = input("Enter zone code (e.g. BEG, INT, ALL): ")
    price = calculate_lift_access_tier(z_input)
    if price is None:
        print("Lift Pass Price: INVALID_INPUT")
    else:
        print("Lift Pass Price: $", price)


if __name__ == "__main__":
    main()
