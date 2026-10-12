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
- **Laptop LLM speed (llama3.2:3b, CPU):** writes ~11.5 tokens/s, reads ~54 tokens/s.
  Most of the time goes to reading the retrieved context, so smaller chunks and top-3 retrieval = faster answers.
- **Where the rule text lives:** `div.field--name-body` (found with browser DevTools → Inspect).
  VARA puts numbering in table cells; leading empty cells = deeper level → kept as indentation for citations.
- **Normalising whitespace before hashing:** spaces/&nbsp; differences must not count as rule changes.
- **Fail loudly:** if the selector stops matching (site redesign), raise an error instead of saving empty text.
- **Bug: silent empty extraction (STAR).** S: tests passed, but real pages gave 0 lines, and comparing
  two empty files said "no differences". T: find why, before it caused false "UNCHANGED" results.
  A: confirmed the page had several elements with the same class and the first was empty; switched to
  "pick the match with the most text", made empty output raise an error, and added a regression test that
  reproduces the bug. R: real text extracted; empty output can never be fingerprinted again.
- **Lesson:** tests on made-up data can miss real-world quirks. Always check outputs on real data too.
