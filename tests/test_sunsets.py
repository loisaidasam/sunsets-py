
import datetime

import sunsets


def test_import():
    # This just checks if the module exists and has no syntax errors
    assert sunsets is not None


def test_new_york():
    cal = sunsets.make_calendar(
        sunsets.Location(
            name="New York, NY",
            latitude=40.7128,
            longitude=-74.0060,
            timezone="America/New_York",
        ),
        start_date=sunsets.date(2026, 1, 1),
        end_date=sunsets.date(2026, 12, 31),
    )
    assert len(cal.events) == 365
    for event in cal.events:
        assert event.name == "Sunset — New York, NY"
        # `event.begin` is an Arrow object; use its .datetime for comparisons
        begin_dt = getattr(event.begin, "datetime", event.begin)
        if begin_dt.date() == datetime.date(2026, 1, 1):
            assert event.name == "Sunset — New York, NY"
            expected = """Daylight: 9:18:49
Sunrise: 2026-01-01 07:20:20 EST
Sunset: 2026-01-01 16:39:10 EST
Location: New York, NY (40.7128, -74.006)"""
            assert event.description == expected
            assert event.begin.isoformat() == "2026-01-01T16:39:10.142530-05:00"
            assert event.duration.total_seconds() == 1800
        elif begin_dt.date() == datetime.date(2026, 12, 31):
            # sanity check for last day
            assert event.name == "Sunset — New York, NY"
            expected = """Daylight: 9:17:57
Sunrise: 2026-12-31 07:20:10 EST
Sunset: 2026-12-31 16:38:08 EST
Location: New York, NY (40.7128, -74.006)"""
            assert event.description == expected
            assert event.begin.isoformat() == "2026-12-31T16:38:08.503062-05:00"

