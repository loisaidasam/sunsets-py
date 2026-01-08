#!/usr/bin/env python3
"""Generate sunset events and export to an ICS file.

This script is a Python reimplementation of the "Sunsets in Google Calendar"
example. It computes sunset times for one or more locations over a date
range and writes them as calendar events to `sunsets.ics`.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Iterable

from astral import Observer
from astral.sun import sun
from ics import Calendar, Event

from zoneinfo import ZoneInfo


@dataclass
class Location:
    name: str
    latitude: float
    longitude: float
    timezone: str

# TODO: Modify this location as desired
# location = Location(name="San Francisco, CA", latitude=37.7749, longitude=-122.4194, timezone="America/Los_Angeles"),
location = Location(name="New York, NY", latitude=40.7128, longitude=-74.0060, timezone="America/New_York"),

def daterange(start_date: date, end_date: date) -> Iterable[date]:
    """Yield dates from start_date to end_date inclusive."""
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)


def compute_sunset(loc: Location, for_date: date) -> datetime:
    """Return the local datetime of the sunset for `loc` on `for_date`.

    Uses `astral.sun.sun` which returns UTC-aware datetimes; we convert to
    the location's timezone.
    """
    observer = Observer(latitude=loc.latitude, longitude=loc.longitude)
    s = sun(observer, date=for_date)
    # astral returns datetimes in UTC by default; convert to zoneinfo
    sunset_utc = s["sunset"]
    # convert to the location timezone
    tz = ZoneInfo(loc.timezone)
    return sunset_utc.astimezone(tz)


def make_calendar(location: Location, start_date: date, end_date: date) -> Calendar:
    cal = Calendar()
    for single_date in daterange(start_date, end_date):
        try:
            sunset_dt = compute_sunset(location, single_date)
        except Exception as e:  # pragma: no cover
            print(f"Failed to compute sunset for {location.name} on {single_date}: {e}")
            continue
        ev = Event()
        ev.name = f"Sunset — {location.name}"
        # Start at sunset; make a 30-minute event
        ev.begin = sunset_dt
        ev.duration = timedelta(minutes=30)
        ev.description = f"Sunset at {sunset_dt.isoformat()} for {location.name}"
        cal.events.add(ev)
    return cal


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate sunset events for a full year")
    parser.add_argument("--year", type=int, default=None, help="Year to generate events for (defaults to current year)")
    parser.add_argument("--out", type=str, default="sunsets.ics", help="Output ICS path")
    args = parser.parse_args()

    year = args.year or datetime.now().year
    start = date(year, 1, 1)
    end = date(year, 12, 31)

    cal = make_calendar(location, start, end)

    out_path = args.out
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(cal)

    print(f"Wrote {len(cal.events)} events for {year} to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
