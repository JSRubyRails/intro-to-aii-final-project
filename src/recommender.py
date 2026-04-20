from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

def _get_client():
    from google import genai
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY not set. Copy .env.example to .env and add your key.")
    return genai.Client(api_key=api_key)


def ai_explain(user: "UserProfile", song: "Song") -> str:
    client = _get_client()
    prompt = (
        f"In one sentence, explain why '{song.title}' by {song.artist} "
        f"({song.genre}, {song.mood}, energy {song.energy}) suits a listener "
        f"who enjoys {user.favorite_genre} music with a {user.favorite_mood} mood "
        f"and target energy of {user.target_energy}."
    )
    return client.models.generate_content(model="gemma-3-1b-it", contents=prompt).text.strip()


def ai_critique_summary(log: List[str]) -> str:
    import time
    time.sleep(2)
    client = _get_client()
    prompt = (
        f"A music recommender ran a self-critique loop and produced this log:\n"
        f"{chr(10).join(log)}\n\n"
        f"In 2-3 sentences, explain: what bias was detected, which songs were removed and why, "
        f"and which songs replaced them and what they bring to the list."
    )
    return client.models.generate_content(model="gemma-3-1b-it", contents=prompt).text.strip()

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
        scored = []
        for song in self.songs:
            score = 0.0
            if song.genre == user.favorite_genre:
                score += 2.0
            if song.mood == user.favorite_mood:
                score += 1.0
            score += 1.0 - abs(song.energy - user.target_energy)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre match ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood match ({song.mood})")
        energy_diff = abs(song.energy - user.target_energy)
        reasons.append(f"energy similarity (diff: {energy_diff:.2f})")
        if user.likes_acoustic and song.acousticness > 0.7:
            reasons.append("acoustic preference matched")
        elif not user.likes_acoustic and song.acousticness < 0.3:
            reasons.append("non-acoustic preference matched")
        return " | ".join(reasons) if reasons else "General match"

    def detect_bias(self, recommended_songs: List[Song]) -> str:
        from collections import Counter
        genres = [s.genre for s in recommended_songs]
        artists = [s.artist for s in recommended_songs]
        moods = [s.mood for s in recommended_songs]
        genre_counts = Counter(genres)
        artist_counts = Counter(artists)
        mood_counts = Counter(moods)
        k = len(recommended_songs)
        bias_msgs = []
        for label, counts in [("genre", genre_counts), ("artist", artist_counts), ("mood", mood_counts)]:
            most_common, count = counts.most_common(1)[0]
            if count / k > 0.7:
                bias_msgs.append(f"Bias detected: {label} '{most_common}' dominates ({count}/{k})")
        return "; ".join(bias_msgs) if bias_msgs else "No significant bias detected."

    def recommend_with_critique(self, user: UserProfile, k: int = 5) -> Tuple[List[Song], List[str]]:
        from collections import Counter
        log = []

        results = self.recommend(user, k)
        bias_report = self.detect_bias(results)
        log.append(f"Pass 1: {bias_report}")

        if bias_report == "No significant bias detected.":
            return results, log

        def base_score(song: Song) -> float:
            score = 0.0
            if song.genre == user.favorite_genre:
                score += 2.0
            if song.mood == user.favorite_mood:
                score += 1.0
            score += 1.0 - abs(song.energy - user.target_energy)
            return score

        scored = sorted(self.songs, key=base_score, reverse=True)
        reranked = []
        genre_counts = Counter()
        for song in scored:
            if genre_counts[song.genre] < 2:
                reranked.append(song)
                genre_counts[song.genre] += 1
            if len(reranked) == k:
                break
        new_bias = self.detect_bias(reranked)
        log.append(f"Pass 2 (after re-rank): {new_bias}")

        swapped_in = [s for s in reranked if s not in results]
        swapped_out = [s for s in results if s not in reranked]
        for out, into in zip(swapped_out, swapped_in):
            log.append(
                f"Removed '{out.title}' ({out.genre}, {out.mood}) → "
                f"Added '{into.title}' ({into.genre}, {into.mood}) "
                f"to reduce {out.genre} dominance"
            )

        return reranked, log

    def evaluate_metrics(self, recommended_songs: List[Song], user: UserProfile, user_history: Optional[List[int]] = None) -> dict:
        genres = set(s.genre for s in recommended_songs)
        artists = set(s.artist for s in recommended_songs)
        diversity = len(genres) + len(artists)
        novelty = None
        if user_history is not None:
            unheard = [s for s in recommended_songs if s.id not in user_history]
            novelty = len(unheard) / len(recommended_songs) if recommended_songs else 0.0
        return {"genre_diversity": len(genres), "artist_diversity": len(artists), "diversity_score": diversity, "novelty": novelty}

def load_songs(csv_path: str) -> List[Dict]:
    """Reads a CSV file and returns a list of song dicts with typed numeric values."""
    import csv

    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(dict(row))
    return songs

def score_song(user_prefs: Dict, song: Dict) -> float:
    """
    Scores a single song against a user preference profile.
    Recipe (max 4.0):
      +2.0  genre match
      +1.0  mood match
      +0-1  energy similarity: 1.0 - abs(song.energy - target_energy)
    """
    score = 0.0
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
    score += 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    return score

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    results = []
    for song, score in scored[:k]:
        reasons = []
        if song["genre"] == user_prefs["favorite_genre"]:
            reasons.append("genre match (+2.0)")
        if song["mood"] == user_prefs["favorite_mood"]:
            reasons.append("mood match (+1.0)")
        energy_points = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
        reasons.append(f"energy similarity +{energy_points:.2f} (song: {song['energy']}, target: {user_prefs['target_energy']})")
        explanation = " | ".join(reasons)
        results.append((song, score, explanation))
    return results
