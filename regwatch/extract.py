"""Turn a downloaded VARA rulebook page (HTML) into clean rule text.

Only the rule itself is kept: menus, sidebars, version lists and footers are dropped.
The numbering (1., a., i.) is kept as indentation so answers can cite exact provisions.
"""
import re
from pathlib import Path

from bs4 import BeautifulSoup

RAW_DIR = Path("data") / "raw"
TEXT_DIR = Path("data") / "text"
BODY_SELECTOR = "div.field--name-body"   # the element that holds the rule text on VARA pages
TITLE_SELECTOR = "h2.page-title"
INDENT = "  "


def clean_spaces(text: str) -> str:
    """Collapse runs of spaces, tabs and non-breaking spaces into one normal space."""
    return re.sub(r"\s+", " ", text).strip()


def row_to_line(row) -> str:
    """Convert one table row of a rule into one line of text.

    VARA lays out numbering in table cells, e.g. ["", "a.", "VARA may issue Rules..."].
    Each empty cell at the start means one level deeper, so it becomes indentation.
    """
    cells = [clean_spaces(cell.get_text(" ")) for cell in row.find_all("td", recursive=False)]
    depth = 0
    while depth < len(cells) and cells[depth] == "":
        depth += 1
    words = " ".join(cell for cell in cells[depth:] if cell)
    return INDENT * depth + words if words else ""


def extract_rule_text(html: str) -> str:
    """Return the cleaned rule text of one page. Raises ValueError if the rule body is missing."""
    soup = BeautifulSoup(html, "html.parser")
    # A page can contain several elements with this class (e.g. small empty blocks
    # elsewhere on the page). The rule itself is the one with the most text.
    candidates = soup.select(BODY_SELECTOR)
    if not candidates:
        raise ValueError(f"No element matching '{BODY_SELECTOR}' found; has the page layout changed?")
    body = max(candidates, key=lambda element: len(element.get_text(strip=True)))

    rows = body.find_all("tr")
    if rows:
        lines = [row_to_line(row) for row in rows]
    else:
        lines = [clean_spaces(line) for line in body.get_text("\n").splitlines()]

    text = "\n".join(line for line in lines if line.strip())
    if not text:
        raise ValueError("Rule body found but it contains no text; refusing to save an empty document.")
    return text


def extract_title(html: str) -> str:
    """Return the section title shown at the top of the page, or '' if there is none."""
    title = BeautifulSoup(html, "html.parser").select_one(TITLE_SELECTOR)
    return clean_spaces(title.get_text(" ")) if title else ""


def main() -> None:
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    for raw_file in sorted(RAW_DIR.glob("*.html")):
        html = raw_file.read_text(encoding="utf-8")
        try:
            text = extract_rule_text(html)
        except ValueError as error:
            print(f"SKIPPED  {raw_file.name}: {error}")
            continue
        out_file = TEXT_DIR / (raw_file.stem + ".txt")
        out_file.write_text(text, encoding="utf-8")
        print(f"EXTRACTED  {out_file.name}  {len(text.splitlines())} lines, {len(text):,} characters")


if __name__ == "__main__":
    main()