from datetime import datetime
from zoneinfo import ZoneInfo

from sunsets import create_description, Location


DESC_EXPECTED = """Daylight: 10:15:00
Sunrise: 2026-01-01 07:30:00 EST
Sunset: 2026-01-01 17:45:00 EST
Location: New York, NY (40.7128, -74.006)"""


def test_create_description_basic():
    # Use New York defaults
    loc = Location(name="New York, NY", latitude=40.7128, longitude=-74.0060, timezone="America/New_York")
    sunrise = datetime(2026, 1, 1, 7, 30, tzinfo=ZoneInfo("America/New_York"))
    sunset = datetime(2026, 1, 1, 17, 45, tzinfo=ZoneInfo("America/New_York"))
    desc = create_description(loc, sunrise, sunset)
    assert desc == DESC_EXPECTED
