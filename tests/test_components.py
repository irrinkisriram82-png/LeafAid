from ui import components


def test_user_values_are_escaped():
    markup = components.profile_card("<script>alert(1)</script>", 'a"@b.com')
    assert "<script>" not in markup
    assert "&lt;script&gt;" in markup


def test_hero_escapes_name():
    assert "<img" not in components.hero_banner("<img src=x onerror=1>")


def test_stats_row_shows_numbers():
    markup = components.stats_row(3, 2, 1)
    assert ">3<" in markup and ">2<" in markup and ">1<" in markup


def test_no_blank_lines_that_break_markdown():
    assert "\n\n" not in components.landing_hero([("📸", "T", "D")])
    assert "\n\n" not in components.hero_banner("Ravi")
