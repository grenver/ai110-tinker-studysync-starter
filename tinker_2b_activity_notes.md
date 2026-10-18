# Tinker 2B activity notes

## Part 1: The counter that forgets

A Streamlit rerun executes the whole script again after an interaction, so
the local broken counter resets to zero, while `st.session_state.fixed_count`
persists between reruns in the same user session. The fixed counter is
initialized only when its key is absent and increments on each fixed-button click.

## Part 2: Validate before you store

Validation rejects empty or whitespace-only subjects and durations of zero
or less before appending. Each failure displays a specific error. Valid
subjects are stripped of surrounding whitespace before storage.
An additional breaker input is a subject containing only spaces; another is
a negative duration with an otherwise valid subject.

## Part 3: Plain class vs. dataclass

`SessionDC` declares the same three fields as `PlainSession`, including the
default priority of `"medium"`. `@dataclass` generates `__init__`, `__repr__`,
and field-based `__eq__` automatically. `print(session_dc)` in the standalone
demo shows the generated representation: the values match the plain class,
with `SessionDC` as the class name. The dataclass needs field declarations
instead of a hand-written initializer and representation method.

## Part 4: Recurrence and conflicts

`next_occurrence` uses `FREQUENCY_DAYS` and `timedelta` to add one day for
daily recurrence or seven days for weekly recurrence. From January 1, 2026,
the results are January 2 and January 8.

Conflict detection compares each pair once and returns every pair with
the same slot. The example flags Calc II and Chem Lab at 08:00. Empty input
returns `[]` because neither loop runs. This matters for a new user's empty
schedule, which should report no conflicts instead of crashing.
