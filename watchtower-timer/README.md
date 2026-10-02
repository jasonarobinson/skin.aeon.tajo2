# Watchtower Study Timer

A single-page, phone-friendly timer for conducting the Watchtower Study and ending on time.
Open `index.html` in Safari (iPhone) or Chrome (Android). Use **Share → Add to Home Screen** to launch it like an app.

- Opens on the current week. Tap the date to pick any other week from the calendar.
- On the meeting day (Saturday by default), from 2 hours before the usual end time (12:40 PM), the study ends at 12:40 PM. Any other time it ends 60 minutes after Start. Tap the end time on the main screen to set a custom one for today.
- Each week's title, paragraph count, review questions and grouped paragraphs load automatically when official data is available; anything you change in setup overrides it.
- Tap the paragraph number you are on (or **Next**). The remaining time is split again across what is left.
- The clock never advances on its own. It flashes amber near the end of a paragraph's time and red when over.
- Custom times per paragraph or review question are capped so they never exceed the total.

## Lesson data

`fetch_lessons.py` reads each week's study article from wol.jw.org (title, paragraph count,
grouped paragraphs such as 9-10, and review questions). Usage:

    python3 fetch_lessons.py <iso-year> <iso-week> <number-of-weeks> out.json

`lessons.json` is the current snapshot (weeks of Dec 29, 2025 through Feb 22, 2027), keyed by the
Monday of each week. The published timer reads the same data from its `lessons` data store.
