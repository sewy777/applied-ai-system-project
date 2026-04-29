"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

from .recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list) -> None:
    """Prints the top 5 recommendations for a given user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print(f"\n{'=' * 50}")
    print(f"Profile: {profile_name}")
    print(f"Prefs  : {user_prefs}")
    print(f"{'=' * 50}")
    for i, (song, score, explanation, conf) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Score      : {score:.2f}")
        print(f"   Confidence : {conf:.1f}%")
        print(f"   Why        : {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.38},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
        # Adversarial: classical is typically low energy, but user wants high energy + euphoric
        "High-Energy Classical (adversarial)": {"genre": "classical", "mood": "euphoric", "energy": 0.95},
        # Adversarial: edm in our catalog is euphoric, not sad — conflicting preferences
        "Sad EDM (adversarial)": {"genre": "edm", "mood": "sad", "energy": 0.9},
    }

    for name, prefs in profiles.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
