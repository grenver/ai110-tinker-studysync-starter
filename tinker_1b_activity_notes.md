# Tinker 1B activity notes

## Part 1: Test first

I tested `session_rating()` even though it already worked so that its expected
boundary behavior is protected while the surrounding code is refactored.
The new assertion verifies that a score of `80` is rated `"Good"`.

## Part 3: Breaker inputs

| Breaker input | Actual result | Decision |
| --- | --- | --- |
| `-5` | `"Skip"` | Flag out of scope: the Session Scorer UI cannot create a negative combined score. |
| `101` | `"Great"` | Flag out of scope: scores produced by the UI are capped at 100 after the streak bonus. |
| `87.5` | `"Good"` | Flag out of scope: the UI sliders and streak input produce whole-number scores. |

## Part 4: Reflection

I moved `apply_streak_bonus()` from `scoring.py` to `scoring_helpers.py` and
verified the imported function kept the demo output unchanged. I accepted the
suggestion to test an exact rating boundary, then verified `80` maps to
`"Good"`; the decimal breaker input mattered because the function accepts it
even though the UI currently cannot produce one.
