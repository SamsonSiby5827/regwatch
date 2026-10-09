# RegWatch: learning notes

## Day 1: fetching and change detection
- **Why hash the cleaned text, not raw HTML?** Raw pages change for irrelevant reasons
  (dates, menus, hidden codes), which would cause false alarms. Hashing only the rule text means
  a changed fingerprint = a changed rule.
- **Four statuses:** NEW (not seen before), CHANGED (fingerprint differs), UNCHANGED (same),
  REMOVED (seen last time, missing now).
- **Polite scraping:** respect robots.txt, wait between requests, identify with a User-Agent,
  download once and cache locally.
- **Data rights:** VARA allows personal non-commercial download but not redistribution, so `data/`
  is git-ignored.