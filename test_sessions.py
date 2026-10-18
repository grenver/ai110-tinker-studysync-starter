from datetime import date

import pytest
from streamlit.testing.v1 import AppTest

from sessions import SessionDC, find_conflicts, next_occurrence


@pytest.mark.parametrize("frequency, expected", [
    ("daily", date(2026, 1, 2)), ("weekly", date(2026, 1, 8)),
])
def test_recurrence(frequency, expected):
    assert next_occurrence(date(2026, 1, 1), frequency) == expected


def test_recurrence_crosses_year_boundary():
    assert next_occurrence(date(2026, 12, 31), "daily") == date(2027, 1, 1)


def test_conflicts_include_every_pair_once():
    a, b, c = [{"subject": name, "slot": "08:00"} for name in "ABC"]
    other = {"subject": "D", "slot": "09:00"}
    assert find_conflicts([a, b, c, other]) == [(a, b), (a, c), (b, c)]
    assert find_conflicts([]) == []
    assert find_conflicts([a]) == []
    assert find_conflicts([a, other]) == []


def test_dataclass_generated_methods():
    session = SessionDC("Math", 30)
    assert session.priority == "medium"
    assert session == SessionDC("Math", 30)
    assert repr(session) == "SessionDC(subject='Math', minutes=30, priority='medium')"


def session_log():
    return AppTest.from_string(
        "from sessions import render_session_log_tab\nrender_session_log_tab()",
        default_timeout=60,
    ).run()


def test_counter_survives_reruns():
    app = session_log()
    for expected in range(1, 4):
        app.button[1].click().run()
        assert app.metric[1].value == str(expected)
    app.button[0].click().run()
    assert app.metric[0].value == "1"
    app.run()
    assert app.metric[0].value == "0"
    assert app.metric[1].value == "3"
    assert not app.exception


@pytest.mark.parametrize("subject, duration, message", [
    ("", 30, "Subject"), ("   ", 30, "Subject"),
    ("Math", 0, "Duration"), ("Math", -5, "Duration"),
])
def test_invalid_input_is_not_stored(subject, duration, message):
    app = session_log()
    app.text_input[0].set_value(subject)
    app.number_input[0].set_value(duration)
    app.button[2].click().run()
    assert message in app.error[0].value
    assert app.session_state["mini_sessions"] == []
    assert not app.exception


def test_valid_session_and_conflict_button():
    app = session_log()
    app.text_input[0].set_value("  Math  ")
    app.number_input[0].set_value(45)
    app.button[2].click().run()
    assert app.session_state["mini_sessions"] == [{"subject": "Math", "duration": 45}]
    assert not app.error
    app.button[3].click().run()
    assert not app.exception


def test_full_app_has_three_tabs():
    app = AppTest.from_file("app.py", default_timeout=60).run()
    assert not app.exception
    assert [tab.label for tab in app.tabs] == [
        "Session Scorer", "Session Log", "Find a Study Spot"
    ]
