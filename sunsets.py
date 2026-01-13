#!/usr/bin/env python3
"""Generate sunset events and export to an ICS file.
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


def daterange(start_date: date, end_date: date) -> Iterable[date]:
    """Yield dates from start_date to end_date inclusive."""
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)


def compute_sun_times(loc: Location, for_date: date):
    """Return (sunrise_dt, sunset_dt) localized to loc.timezone.
    """
    observer = Observer(latitude=loc.latitude, longitude=loc.longitude)
    s = sun(observer, date=for_date)
    tz = ZoneInfo(loc.timezone)
    sunrise = s["sunrise"].astimezone(tz)
    sunset = s["sunset"].astimezone(tz)
    return sunrise, sunset


def create_description(location: Location, sunrise_dt: datetime, sunset_dt: datetime) -> str:
    """Return a human-friendly, multi-line description for an event.
    """
    daylight = sunset_dt - sunrise_dt
    hrs, rem = divmod(int(daylight.total_seconds()), 3600)
    mins, secs = divmod(rem, 60)
    daylight_str = f"{hrs}:{mins:02d}:{secs:02d}"
    desc_lines = [
        f"Daylight: {daylight_str}",
        f"Sunrise: {sunrise_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}",
        f"Sunset: {sunset_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}",
        f"Location: {location.name} ({location.latitude}, {location.longitude})",
    ]
    return "\n".join(desc_lines)


def make_event(location: Location, sunrise_dt: datetime, sunset_dt: datetime) -> Event:
    """Create and return an `ics.Event` for the given date and sun times."""
    ev = Event()
    ev.name = f"Sunset — {location.name}"
    ev.begin = sunset_dt
    ev.duration = timedelta(minutes=30)
    ev.description = create_description(location, sunrise_dt, sunset_dt)
    return ev


def make_calendar(location: Location, start_date: date, end_date: date) -> Calendar:
    cal = Calendar()
    for row_num, single_date in enumerate(daterange(start_date, end_date), start=1):
        try:
            sunrise_dt, sunset_dt = compute_sun_times(location, single_date)
        except Exception as e:  # pragma: no cover
            print(f"Failed to compute sunset for {location.name} on {single_date}: {e}")
            raise
        ev = make_event(location, sunrise_dt, sunset_dt)
        if row_num == 1:
            print(f"Sample event description:\n{ev.description}\n")
        cal.events.add(ev)
    return cal


def parse_args():
    parser = argparse.ArgumentParser(description="Generate sunset events for a full year")
    year_default = datetime.now().year
    parser.add_argument("--year", type=int, default=year_default, help=f"Year to generate events for (defaults to current year, {year_default})")
    parser.add_argument("--out", type=str, default="sunsets.ics", help="Output ICS path (default 'sunsets.ics')")
    # Location inputs (single location only)
    parser.add_argument("--name", type=str, default="New York, NY", help="Location name for event title (default 'New York, NY')")
    parser.add_argument("--lat", type=float, default=40.7128, help="Latitude for the location (default 40.7128)")
    parser.add_argument("--lon", type=float, default=-74.0060, help="Longitude for the location (default -74.0060)")
    parser.add_argument("--tz", type=str, default="America/New_York", help="Timezone name for the location (IANA) (default 'America/New_York')")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    location = Location(name=args.name, latitude=args.lat, longitude=args.lon, timezone=args.tz)
    year = args.year
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
