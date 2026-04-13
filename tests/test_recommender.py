from src.recommender import Song, UserProfile, Recommender, load_songs, score_song, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# ── Adversarial / edge-case tests ─────────────────────────────────────────

SONGS = load_songs("data/songs.csv")


def test_contradictory_profile_returns_k_results():
    """High energy + sad folk mood: conflicting numeric and categorical signals."""
    user = {
        "favorite_genres": ["folk"],
        "favorite_moods":  ["sad"],
        "target_energy":       0.92,
        "target_acousticness": 0.80,
        "target_tempo":        170,
    }
    results = recommend_songs(user, SONGS, k=5)
    assert len(results) == 5


def test_out_of_range_tempo_does_not_crash():
    """Tempo of 200 BPM exceeds dataset max of 178 — normalization must not crash."""
    user = {
        "favorite_genres": ["electronic"],
        "favorite_moods":  ["euphoric"],
        "target_energy":       0.90,
        "target_acousticness": 0.05,
        "target_tempo":        200,
    }
    score, _ = score_song(user, SONGS[0])
    assert isinstance(score, float)


def test_unknown_genre_mood_categorical_score_is_zero():
    """Genre/mood absent from dataset — every song should report 'no match'."""
    user = {
        "favorite_genres": ["k-pop"],
        "favorite_moods":  ["zen"],
        "target_energy":       0.55,
        "target_acousticness": 0.50,
        "target_tempo":        100,
    }
    for song in SONGS:
        _, reasons = score_song(user, song)
        genre_reason = next(r for r in reasons if r.startswith("genre"))
        mood_reason  = next(r for r in reasons if r.startswith("mood"))
        assert "no match" in genre_reason
        assert "no match" in mood_reason


def test_midpoint_profile_scores_cluster():
    """All-neutral targets: scores should cluster within a narrow band (<0.60 spread)."""
    user = {
        "favorite_genres": ["pop"],
        "favorite_moods":  ["happy"],
        "target_energy":       0.50,
        "target_acousticness": 0.50,
        "target_tempo":        116,
    }
    scores = [score_song(user, s)[0] for s in SONGS]
    assert max(scores) - min(scores) < 0.60


def test_empty_lists_do_not_crash():
    """Empty genre/mood lists: scoring must not raise and must return 5 reasons."""
    user = {
        "favorite_genres": [],
        "favorite_moods":  [],
        "target_energy":       0.40,
        "target_acousticness": 0.80,
        "target_tempo":        78,
    }
    score, reasons = score_song(user, SONGS[0])
    assert isinstance(score, float)
    assert len(reasons) == 5
