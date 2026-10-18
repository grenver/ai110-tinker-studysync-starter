# Tinker 3B: Rank & Explain

## Load and score

The csv module loads all 10 spots with DictReader. Distance becomes a float
and seats become an int. Leaving distance as a string would cause a TypeError
when comparing it with the numeric profile max_distance in score_study_spot.

Weighted scoring awards +3 for acceptable noise, +2 for acceptable distance,
and +1 for enough seats; each mismatch subtracts the same weight. Noise matters
most because supporting concentration is our chosen priority. This is a design
choice, not a universal student preference.

For the default profile (moderate noise, 1 mile, 4 seats), Innovation Commons
scores 3 + 2 + 1 = 6; Courtyard Cafe scores -3 + 2 + 1 = 0; North Stacks Nook
scores 3 - 2 + 1 = 2. Reasons describe all three factors using actual spot data.

## Ranking and output

Every spot is scored before sorted(key=..., reverse=True) ranks the collection.
Slicing [:k] selects the top-k. Ascending sorting would put the lowest scores
first. Equal scores preserve CSV order, so the default top three are Innovation
Commons, Grand Reading Room, and Engineering Lounge, each scoring 6.
The script prints three explained lines; Streamlit uses the same logic.

## Bias and filter bubble

Giving noise more weight than distance creates a filter bubble by repeatedly
burying close-but-noisy spots below quieter, farther spots, narrowing what the
user sees even when the scores correctly follow the formula.

Students with mobility limitations or short breaks between classes may be
underserved: Student Union Tables is only 0.1 miles away but scores 0 under the
default profile, below North Stacks Nook at 1.2 miles with a score of 2.
Allowing students to choose weights or showing a nearby alternative could
broaden exposure. CSV-order tie breaking also favors earlier rows when more
than three spots share the highest score.

## Pipeline diagram

diagram.mmd traces CSV input, numeric conversion, profile-based scoring,
descending ranking, top-k selection, and explained output. A flowchart shows
how data moves through operations; a class diagram shows types, attributes,
methods, and relationships. Preview diagram.mmd to compare with ranking.py.
