import pytest

from regwatch.extract import extract_rule_text, extract_title

# A tiny made-up page with the same layout as a VARA rulebook page.
# (Invented text: real regulator text is never copied into the repo.)
FAKE_PAGE = """
<html><body>
  <nav>Main menu: Home | Rulebooks | Search</nav>
  <h2 class="page-title"><span>Z. Example   Section</span></h2>
  <div class="palette-container"><a href="/old">Jan 01 2024 - Jun 30 2024</a></div>
  <div class="field field--name-body">
    <table><tbody>
      <tr><td>1.</td><td colspan="4"><u>Scope.</u> These rules apply to Example Firms.</td></tr>
      <tr><td>&nbsp;</td><td>a.</td><td colspan="4">Firms must keep records;<br>&nbsp;</td></tr>
      <tr><td>&nbsp;</td><td>&nbsp;</td><td>i.</td><td colspan="4">for   five years.</td></tr>
      <tr><td>&nbsp;</td><td>&nbsp;</td></tr>
    </tbody></table>
  </div>
  <footer>Copyright 2026. All rights reserved.</footer>
</body></html>
"""


def test_keeps_numbering_as_indentation():
    assert extract_rule_text(FAKE_PAGE).splitlines() == [
        "1. Scope. These rules apply to Example Firms.",
        "  a. Firms must keep records;",
        "    i. for five years.",
    ]


def test_drops_menus_versions_and_footer():
    text = extract_rule_text(FAKE_PAGE)
    for unwanted in ["Main menu", "Jan 01 2024", "Copyright"]:
        assert unwanted not in text


def test_extra_spaces_do_not_change_the_text():
    # Same rule, messier spacing: the cleaned text (and so the hash) must be identical.
    messy = FAKE_PAGE.replace("Firms must keep", "Firms   must&nbsp;keep")
    assert extract_rule_text(messy) == extract_rule_text(FAKE_PAGE)


def test_missing_rule_body_raises_clear_error():
    with pytest.raises(ValueError):
        extract_rule_text("<html><body><p>Page not found</p></body></html>")


def test_extract_title():
    assert extract_title(FAKE_PAGE) == "Z. Example Section"


def test_picks_the_real_rule_body_when_several_match():
    # Bug found on the real VARA page: an empty block with the same class appeared first.
    page_with_decoy = FAKE_PAGE.replace(
        "<nav>", '<div class="field--name-body"></div><nav>'
    )
    assert extract_rule_text(page_with_decoy) == extract_rule_text(FAKE_PAGE)


def test_empty_rule_body_raises_instead_of_saving_nothing():
    with pytest.raises(ValueError):
        extract_rule_text('<div class="field--name-body"><p>&nbsp;</p></div>')