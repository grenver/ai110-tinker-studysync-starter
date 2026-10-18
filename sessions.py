"""
StudySync -- Session Log (Ticket 2, Tinker 2B).

Demonstrates persistent counters, input validation, dataclasses,
recurring dates, and pairwise conflict detection.
"""

from dataclasses import dataclass
from datetime import date, timedelta

FREQUENCY_DAYS = {"daily": 1, "weekly": 7}


class PlainSession:
    def __init__(self, subject, minutes, priority="medium"):
        self.subject = subject
        self.minutes = minutes
        self.priority = priority

    def __repr__(self):
        return f"PlainSession(subject={self.subject!r}, minutes={self.minutes}, priority={self.priority!r})"


@dataclass
class SessionDC:
    subject: str
    minutes: int
    priority: str = "medium"


def next_occurrence(last_date: date, frequency: str) -> date:
    """
    Return the next scheduled date given the last session date and a
    frequency label ("daily" or "weekly"), using FREQUENCY_DAYS and timedelta.
    """
    return last_date + timedelta(days=FREQUENCY_DAYS[frequency])


def find_conflicts(sessions: list) -> list:
    """
    sessions: list of dicts, each with a "slot" key, e.g. {"subject": "Calc II", "slot": "08:00"}.

    Return a list of (session_a, session_b) tuples for every pair that shares
    the same "slot". Must NOT crash on an empty list or a list with no conflicts.
    """
    conflicts = []
    for index, session_a in enumerate(sessions):
        for session_b in sessions[index + 1:]:
            if session_a["slot"] == session_b["slot"]:
                conflicts.append((session_a, session_b))
    return conflicts


def render_session_log_tab():
    import streamlit as st

    st.subheader("Parts 1-2: Log a Session")

    # BUG (Part 1): this is a plain local variable, so Streamlit "forgets" it on every rerun.
    count = 0
    if st.button("Log a session (broken)"):
        count += 1
    st.metric("Sessions logged (broken)", count)

    if "fixed_count" not in st.session_state:
        st.session_state.fixed_count = 0
    if st.button("Log a session (fixed)"):
        st.session_state.fixed_count += 1
    st.metric("Sessions logged (fixed)", st.session_state.fixed_count)

    st.divider()
    st.subheader("Part 2: Session List (with validation)")

    if "mini_sessions" not in st.session_state:
        st.session_state.mini_sessions = []

    subject = st.text_input("Subject")
    duration = st.number_input("Duration (minutes)", value=30, step=1)

    if st.button("Add session"):
        if not subject.strip():
            st.error("Subject must not be empty or whitespace-only.")
        elif duration <= 0:
            st.error("Duration must be greater than 0 minutes.")
        else:
            st.session_state.mini_sessions.append(
                {"subject": subject.strip(), "duration": duration}
            )

    st.write(st.session_state.mini_sessions)

    st.divider()
    st.subheader("Part 4: Conflict Check")
    if st.button("Check for time conflicts"):
        sample = [
            {"subject": "Calc II", "slot": "08:00"},
            {"subject": "Chem Lab", "slot": "08:00"},
            {"subject": "History", "slot": "09:00"},
        ]
        conflicts = find_conflicts(sample)
        st.write(conflicts if conflicts else "No conflicts found.")


if __name__ == "__main__":
    plain = PlainSession("Study group: Calc II", 45, priority="high")
    print(plain)
    session_dc = SessionDC("Study group: Calc II", 45, priority="high")
    print(session_dc)

    print(next_occurrence(date(2026, 1, 1), "daily"))
    print(next_occurrence(date(2026, 1, 1), "weekly"))

    print(
        find_conflicts(
            [
                {"subject": "Calc II", "slot": "08:00"},
                {"subject": "Chem Lab", "slot": "08:00"},
                {"subject": "History", "slot": "09:00"},
            ]
        )
    )
    print(find_conflicts([]))
