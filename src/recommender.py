from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a CSV of songs and return a list of dicts with typed values."""
    
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    int(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a weighted similarity score (0–1) and a list of per-feature reason strings."""
    weights = {
        "energy":       0.30,
        "acousticness": 0.25,
        "tempo":        0.20,
        "mood":         0.15,
        "genre":        0.10,
    }

    # weights = {
    #     "energy":       0.60,
    #     "acousticness": 0.25,
    #     "tempo":        0.20,
    #     "mood":         0.15,
    #     "genre":        0.05,
    # }

    # Normalize tempo to [0, 1] using the dataset range (54–178 BPM)
    TEMPO_MIN, TEMPO_MAX = 54, 178
    song_tempo_norm   = (song["tempo_bpm"]          - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    target_tempo_norm = (user_prefs["target_tempo"] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)

    reasons = []
    score = 0.0

    # --- Numeric features: 1 - |song - target| ---
    energy_score = 1 - abs(song["energy"] - user_prefs["target_energy"])
    score += weights["energy"] * energy_score
    reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f}")

    acousticness_score = 1 - abs(song["acousticness"] - user_prefs["target_acousticness"])
    score += weights["acousticness"] * acousticness_score
    reasons.append(f"acousticness {song['acousticness']:.2f} vs target {user_prefs['target_acousticness']:.2f}")

    tempo_score = 1 - abs(song_tempo_norm - target_tempo_norm)
    score += weights["tempo"] * tempo_score
    reasons.append(f"tempo {song['tempo_bpm']} BPM vs target {user_prefs['target_tempo']} BPM")

    # --- Categorical features: 1 if match, 0 if not ---
    mood_match = song["mood"] in user_prefs["favorite_moods"]
    score += weights["mood"] * (1.0 if mood_match else 0.0)
    reasons.append(f"mood {'matched' if mood_match else 'no match'} ({song['mood']})")

    genre_match = song["genre"] in user_prefs["favorite_genres"]
    score += weights["genre"] * (1.0 if genre_match else 0.0)
    reasons.append(f"genre {'matched' if genre_match else 'no match'} ({song['genre']})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank by score descending, and return the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
