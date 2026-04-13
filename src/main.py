"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from tabulate import tabulate
from recommender import load_songs, recommend_songs, score_song


PROFILES = {
    "chill_listener": {
        "favorite_genres": ["lofi", "jazz"],
        "favorite_moods":  ["chill", "relaxed"],
        "target_energy":       0.40,
        "target_acousticness": 0.80,
        "target_tempo":        78,
    },
    "workout_fan": {
        "favorite_genres": ["pop", "electronic"],
        "favorite_moods":  ["intense", "euphoric"],
        "target_energy":       0.90,
        "target_acousticness": 0.05,
        "target_tempo":        130,
    },
    "late_night": {
        "favorite_genres": ["synthwave", "ambient"],
        "favorite_moods":  ["moody", "dreamy"],
        "target_energy":       0.55,
        "target_acousticness": 0.40,
        "target_tempo":        100,
    },
    "amateur_dancer": {
        "favorite_genres": ["latin", "pop", "hip-hop"],
        "favorite_moods":  ["playful", "happy"],
        "target_energy":       0.80,
        "target_acousticness": 0.10,
        "target_tempo":        100,   # moderate — not too fast for a beginner
    },
}

# Switch profiles by changing this one line:
ACTIVE_PROFILE = "chill_listener"


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    user_prefs = PROFILES[ACTIVE_PROFILE]
    print(f"Active profile: {ACTIVE_PROFILE}\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    rows = []
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = "\n".join(f"• {r}" for r in explanation.split(" | "))
        rows.append([
            f"#{i}",
            song["title"],
            song["artist"],
            song["genre"],
            song["mood"],
            f"{score:.2f}",
            reasons,
        ])

    headers = ["Rank", "Title", "Artist", "Genre", "Mood", "Score", "Reasons"]
    print("\n" + tabulate(rows, headers=headers, tablefmt="rounded_grid"))


if __name__ == "__main__":
    main()
