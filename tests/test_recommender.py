import pytest
from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs, validate_user_prefs, confidence


def make_songs():
    return [
        Song(id=1, title="Test Pop Track", artist="Test Artist", genre="pop",
             mood="happy", energy=0.8, tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.2),
        Song(id=2, title="Chill Lofi Loop", artist="Test Artist", genre="lofi",
             mood="chill", energy=0.4, tempo_bpm=80, valence=0.6, danceability=0.5, acousticness=0.9),
    ]


def make_pop_user():
    return UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)


# --- OOP class tests ---

def test_recommend_returns_songs_sorted_by_score():
    user = make_pop_user()
    rec = Recommender(make_songs())
    results = rec.recommend(user, k=2)
    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = make_pop_user()
    rec = Recommender(make_songs())
    explanation = rec.explain_recommendation(user, rec.songs[0])
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_oop_validation_raises_on_bad_energy():
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=1.5, likes_acoustic=False)
    rec = Recommender(make_songs())
    with pytest.raises(ValueError):
        rec.recommend(user)


# --- Functional API tests ---

def test_score_song_genre_match():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {"genre": "pop", "mood": "sad", "energy": 0.8}
    score, reasons = score_song(prefs, song)
    assert score >= 2.0
    assert any("genre match" in r for r in reasons)


def test_score_song_mood_match():
    prefs = {"genre": "rock", "mood": "happy", "energy": 0.5}
    song = {"genre": "pop", "mood": "happy", "energy": 0.5}
    score, reasons = score_song(prefs, song)
    assert any("mood match" in r for r in reasons)


def test_recommend_songs_returns_sorted_results():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    songs = [
        {"genre": "pop", "mood": "happy", "energy": 0.8},
        {"genre": "lofi", "mood": "chill", "energy": 0.4},
    ]
    results = recommend_songs(prefs, songs, k=2)
    assert results[0][1] >= results[1][1]


# --- Validation / guardrail tests ---

def test_validate_rejects_empty_genre():
    with pytest.raises(ValueError, match="genre"):
        validate_user_prefs({"genre": "", "mood": "happy", "energy": 0.5})


def test_validate_rejects_missing_mood():
    with pytest.raises(ValueError, match="mood"):
        validate_user_prefs({"genre": "pop", "mood": "", "energy": 0.5})


def test_validate_rejects_energy_above_1():
    with pytest.raises(ValueError, match="energy"):
        validate_user_prefs({"genre": "pop", "mood": "happy", "energy": 1.5})


def test_validate_rejects_energy_below_0():
    with pytest.raises(ValueError, match="energy"):
        validate_user_prefs({"genre": "pop", "mood": "happy", "energy": -0.1})


# --- Confidence scoring tests ---

def test_confidence_max_score():
    assert confidence(4.0) == 100.0


def test_confidence_zero_score():
    assert confidence(0.0) == 0.0


def test_confidence_partial_score():
    result = confidence(2.0)
    assert result == 50.0
