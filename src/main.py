"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, Song, UserProfile, Recommender, ai_explain, ai_critique_summary


def main() -> None:
    songs = load_songs("data/songs.csv")
    song_objs = [Song(**song) for song in songs]
    recommender = Recommender(song_objs)

    profiles = [
        {
            "name": "Pop Fan",
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": False,
            "history": [1, 5, 10],
        },
        {
            "name": "Chill Listener",
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.4,
            "likes_acoustic": True,
            "history": [2, 4, 9, 20],
        },
        {
            "name": "Workout Mode",
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.95,
            "likes_acoustic": False,
            "history": [3, 14],
        },
        {
            "name": "Classical Enthusiast",
            "favorite_genre": "classical",
            "favorite_mood": "melancholy",
            "target_energy": 0.3,
            "likes_acoustic": True,
            "history": [11, 16, 18],
        },
        {
            "name": "Varied Adventurer",
            "favorite_genre": "varied",
            "favorite_mood": "moody",
            "target_energy": 0.5,
            "likes_acoustic": False,
            "history": [7, 15],
        },
    ]

    for profile in profiles:
        name = profile.pop("name")
        history = profile.pop("history")
        user = UserProfile(**profile)
        recommended, critique_log = recommender.recommend_with_critique(user, k=5)
        print("\n" + "=" * 50)
        print(f"  Top 5 for: {name}")
        print("=" * 50)
        for i, song in enumerate(recommended, start=1):
            explanation = ai_explain(user, song)
            print(f"\n#{i}  {song.title} by {song.artist}")
            print(f"    Why   : {explanation}")
        swap_entries = [e for e in critique_log if e.startswith("Removed")]
        bias_entries = [e for e in critique_log if not e.startswith("Removed")]
        ai_summary = ai_critique_summary(bias_entries)
        print(f"\n  [AI Critique] {ai_summary}")
        for swap in swap_entries:
            print(f"  [Swap] {swap}")
        metrics = recommender.evaluate_metrics(recommended, user, user_history=history)
        print(f"Metrics: {metrics}")
        print("\n" + "=" * 50)
        profile["name"] = name
        profile["history"] = history


if __name__ == "__main__":
    main()
