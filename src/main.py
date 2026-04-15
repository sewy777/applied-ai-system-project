"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

Functions implemented in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    print("-" * 50)
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Score : {score:.2f}")
        print(f"   Why   : {explanation}")
        print()


if __name__ == "__main__":
    main()
