import csv
import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("recommender.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

MAX_POSSIBLE_SCORE = 4.0  # genre(2.0) + mood(1.0) + energy_sim(1.0)


@dataclass
class Song:
    """Represents a song and its attributes."""
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
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool  # reserved for future acoustic scoring; not used in current scoring logic


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs ranked by how well they match the user's taste profile."""
        def _score(song: Song) -> float:
            score = 0.0
            if song.genre == user.favorite_genre:
                score += 2.0
            if song.mood == user.favorite_mood:
                score += 1.0
            score += 1.0 - abs(song.energy - user.target_energy)
            return score

        return sorted(self.songs, key=_score, reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable string explaining why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append("genre match (+2.0)")
        if song.mood == user.favorite_mood:
            reasons.append("mood match (+1.0)")
        energy_sim = round(1.0 - abs(song.energy - user.target_energy), 2)
        reasons.append(f"energy similarity (+{energy_sim:.2f})")
        return ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and returns them as a list of dicts with numeric values converted."""
    songs = []
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["id"] = int(row["id"])
                row["energy"] = float(row["energy"])
                row["tempo_bpm"] = float(row["tempo_bpm"])
                row["valence"] = float(row["valence"])
                row["danceability"] = float(row["danceability"])
                row["acousticness"] = float(row["acousticness"])
                songs.append(dict(row))
        logger.info("Loaded %d songs from %s", len(songs), csv_path)
    except FileNotFoundError:
        logger.error("Song catalog not found: %s", csv_path)
        raise
    except Exception as e:
        logger.error("Failed to load songs: %s", e)
        raise
    return songs


def validate_user_prefs(user_prefs: Dict) -> None:
    """Raises ValueError if user preferences are missing or out of range."""
    if not user_prefs.get("genre"):
        raise ValueError("user_prefs must include a non-empty 'genre'")
    if not user_prefs.get("mood"):
        raise ValueError("user_prefs must include a non-empty 'mood'")
    energy = user_prefs.get("energy")
    if energy is None:
        raise ValueError("user_prefs must include 'energy'")
    if not (0.0 <= energy <= 1.0):
        raise ValueError(f"'energy' must be between 0.0 and 1.0, got {energy}")


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences; returns (total_score, list_of_reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_sim = round(1.0 - abs(song["energy"] - user_prefs.get("energy", 0.5)), 2)
    score += energy_sim
    reasons.append(f"energy similarity (+{energy_sim:.2f})")

    return round(score, 2), reasons


def confidence(score: float) -> float:
    """Returns a confidence percentage (0–100) based on how close a score is to the max possible."""
    return round((score / MAX_POSSIBLE_SCORE) * 100, 1)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str, float]]:
    """
    Scores every song and returns the top k as (song, score, explanation, confidence_pct)
    sorted highest first. Validates user_prefs before running.
    """
    validate_user_prefs(user_prefs)
    logger.info(
        "Running recommendations for genre=%s, mood=%s, energy=%.2f",
        user_prefs.get("genre"),
        user_prefs.get("mood"),
        user_prefs.get("energy", 0.0),
    )

    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        conf = confidence(score)
        scored.append((song, score, explanation, conf))

    results = sorted(scored, key=lambda x: x[1], reverse=True)[:k]
    logger.info("Top result: '%s' (score=%.2f, confidence=%.1f%%)", results[0][0]["title"], results[0][1], results[0][3])
    return results
