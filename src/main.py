"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        {
            "name": "Pop Fan",
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": False,
        },
        {
            "name": "Chill Listener",
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.4,
            "likes_acoustic": True,
        },
        {
            "name": "Workout Mode",
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.95,
            "likes_acoustic": False,
        },
        # --- Adversarial / edge-case profiles ---
        {
            "name": "[ADVERSARIAL] Out-of-range energy (1.5)",
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 1.5,
            "likes_acoustic": True,
        },
        {
            "name": "[ADVERSARIAL] Conflicting high energy + melancholy mood",
            "favorite_genre": "classical",
            "favorite_mood": "melancholy",
            "target_energy": 0.9,
            "likes_acoustic": False,
        },
        {
            "name": "[ADVERSARIAL] Mood not in dataset (sad)",
            "favorite_genre": "pop",
            "favorite_mood": "sad",
            "target_energy": 0.8,
            "likes_acoustic": False,
        },
        {
            "name": "[ADVERSARIAL] Genre not in dataset (k-pop)",
            "favorite_genre": "k-pop",
            "favorite_mood": "happy",
            "target_energy": 0.7,
            "likes_acoustic": False,
        },
        {
            "name": "[ADVERSARIAL] likes_acoustic ignored (folk/nostalgic)",
            "favorite_genre": "folk",
            "favorite_mood": "nostalgic",
            "target_energy": 0.3,
            "likes_acoustic": True,
        },
        {
            "name": "[ADVERSARIAL] Tie-breaking undefined (lofi/chill/energy=0.385)",
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.385,
            "likes_acoustic": True,
        },
    ]

    for profile in profiles:
        name = profile.pop("name")
        recommendations = recommend_songs(profile, songs, k=5)

        print("\n" + "=" * 50)
        print(f"  Top 5 for: {name}")
        print("=" * 50)
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{i}  {song['title']} by {song['artist']}")
            print(f"    Score : {score:.2f} / 4.00")
            print(f"    Why   : {explanation}")
        print("\n" + "=" * 50)
        profile["name"] = name


if __name__ == "__main__":
    main()
