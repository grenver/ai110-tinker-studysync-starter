"""
StudySync -- Find a Study Spot (Ticket 3, Tinker 3B).

Load, score, rank, and explain campus study spots.
"""

import csv

NOISE_ORDER = {"quiet": 0, "moderate": 1, "loud": 2}


def load_study_spots(csv_path: str) -> list:
    """
    Load study spots from a CSV into a list of dicts, converting
    "distance_miles" to float and "seats_available" to int.
    """
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        spots = []
        for row in csv.DictReader(csv_file):
            row["distance_miles"] = float(row["distance_miles"])
            row["seats_available"] = int(row["seats_available"])
            spots.append(row)
    return spots


def score_study_spot(profile: dict, spot: dict) -> tuple:
    """
    Score one study spot against a student profile.

    profile example: {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}

    Return (score, reasons) where reasons is a list of short strings
    explaining what contributed to the score, e.g. ["quiet enough", "close enough"].
    """
    factors = [
        (NOISE_ORDER[spot["noise_level"]] <= NOISE_ORDER[profile["max_noise"]], 3,
         f"noise {spot['noise_level']} (maximum {profile['max_noise']})"),
        (spot["distance_miles"] <= profile["max_distance"], 2,
         f"distance {spot['distance_miles']:g} miles (maximum {profile['max_distance']:g})"),
        (spot["seats_available"] >= profile["min_seats"], 1,
         f"{spot['seats_available']} seats (minimum {profile['min_seats']})"),
    ]
    score = 0.0
    reasons = []
    for matches, weight, description in factors:
        contribution = weight if matches else -weight
        score += contribution
        reasons.append(f"{description}: {'matches' if matches else 'does not match'} ({contribution:+d})")
    return score, reasons


def rank_study_spots(profile: dict, spots: list, k: int = 3) -> list:
    """
    Score every study spot, then return the top k as (spot, score, reasons)
    tuples, sorted by score descending.
    """
    if k < 0:
        raise ValueError("k must be non-negative")
    scored = [(spot, *score_study_spot(profile, spot)) for spot in spots]
    # Stable sorting preserves CSV order for ties.
    return sorted(scored, key=lambda result: result[1], reverse=True)[:k]


def format_results(ranked: list) -> None:
    """Print each ranked study spot with its score and reasons, one line each."""
    for position, (spot, score, reasons) in enumerate(ranked, start=1):
        print(f"{position}. {spot['name']} -- Score: {score:.1f} -- Because: {'; '.join(reasons)}")


def render_study_spot_tab():
    import streamlit as st

    st.subheader("Find a Study Spot")
    max_noise = st.selectbox("Max noise level", ["quiet", "moderate", "loud"], index=1)
    max_distance = st.slider("Max distance (miles)", 0.0, 3.0, 1.0)
    min_seats = st.number_input("Minimum seats needed", min_value=1, value=4, step=1)

    if st.button("Find spots"):
        profile = {"max_noise": max_noise, "max_distance": max_distance, "min_seats": min_seats}
        try:
            spots = load_study_spots("data/study_spots.csv")
            ranked = rank_study_spots(profile, spots, k=3)
            for spot, score, reasons in ranked:
                st.write(f"**{spot['name']}** -- Score: {score:.1f} -- Because: {', '.join(reasons)}")
        except NotImplementedError:
            st.warning("ðŸš§ Ranking isn't implemented yet -- that's Tinker 3B's ticket.")


if __name__ == "__main__":
    spots = load_study_spots("data/study_spots.csv")
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    ranked = rank_study_spots(profile, spots, k=3)
    format_results(ranked)

