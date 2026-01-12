# sunsets-py

Small script to compute daily sunset events for a single location and export them as an ICS calendar file.

A python version of https://hilaryparker.com/2014/05/27/sunsets-in-google-calendar-using-r/

## Install

```bash
uv sync
```

## Usage

Generate an events file for the current year using the default location (New York, NY):

```bash
$ uv run sunsets.py --help
usage: sunsets.py [-h] [--year YEAR] [--out OUT] [--name NAME] [--lat LAT] [--lon LON] [--tz TZ]

Generate sunset events for a full year

options:
  -h, --help   show this help message and exit
  --year YEAR  Year to generate events for (defaults to current year, 2026)
  --out OUT    Output ICS path (default 'sunsets.ics')
  --name NAME  Location name for event title (default 'New York, NY')
  --lat LAT    Latitude for the location (default 40.7128)
  --lon LON    Longitude for the location (default -74.0060)
  --tz TZ      Timezone name for the location (IANA) (default 'America/New_York')
```

## Example output day

```
DTSTART:20260112T224857Z
SUMMARY:Sunset — VaHi\, Atlanta\, GA
UID:0421c9cc-c9e2-44c2-bef4-9b8560a745ff@0421.org
END:VEVENT
BEGIN:VEVENT
DESCRIPTION:Daylight: 10:42:46\nSunrise: 07:30:20 EST\nSunset: 18:13:07 EST\nLocation: Atlanta\, GA
DURATION:PT30M
```

## Notes
- The script uses `astral` to compute sunrise/sunset times and `ics` to build a calendar file.
- Event descriptions include the sunrise time and the daylight duration (sunset - sunrise) when available.

## License

MIT
