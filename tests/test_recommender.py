from src.recommender import Song, UserProfile, Recommender

def make_song(id, genre, mood, energy, artist=None):
    return Song(id=id, title=f"Song {id}", artist=artist or f"Artist {id}", genre=genre, mood=mood,
                energy=energy, tempo_bpm=100, valence=0.5, danceability=0.5, acousticness=0.5)

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


# --- Bias detection ---

def test_detect_bias_flags_dominant_genre():
    songs = [make_song(i, "lofi", "chill", 0.4) for i in range(1, 5)] + \
            [make_song(5, "pop", "happy", 0.8)]
    rec = Recommender([])
    report = rec.detect_bias(songs)
    assert "Bias detected" in report
    assert "lofi" in report

def test_detect_bias_passes_diverse_list():
    songs = [
        make_song(1, "pop", "happy", 0.8),
        make_song(2, "lofi", "chill", 0.4),
        make_song(3, "rock", "intense", 0.9),
        make_song(4, "jazz", "relaxed", 0.5),
        make_song(5, "classical", "melancholy", 0.3),
    ]
    rec = Recommender([])
    report = rec.detect_bias(songs)
    assert report == "No significant bias detected."

# --- Critique loop ---

def test_critique_loop_resolves_bias():
    biased_songs = [make_song(i, "lofi", "chill", 0.4 + i * 0.01) for i in range(1, 5)]
    diverse_songs = [
        make_song(5, "pop", "happy", 0.8),
        make_song(6, "rock", "intense", 0.9),
        make_song(7, "jazz", "relaxed", 0.5),
    ]
    rec = Recommender(biased_songs + diverse_songs)
    user = UserProfile(favorite_genre="lofi", favorite_mood="chill", target_energy=0.4, likes_acoustic=True)
    results, log = rec.recommend_with_critique(user, k=5)
    final_bias = rec.detect_bias(results)
    assert final_bias == "No significant bias detected."

def test_critique_loop_skips_rerank_when_no_bias():
    songs = [
        make_song(1, "pop", "happy", 0.8),
        make_song(2, "lofi", "chill", 0.4),
        make_song(3, "rock", "intense", 0.9),
        make_song(4, "jazz", "relaxed", 0.5),
        make_song(5, "classical", "melancholy", 0.3),
    ]
    rec = Recommender(songs)
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    _, log = rec.recommend_with_critique(user, k=5)
    assert len(log) == 1
    assert "No significant bias" in log[0]

# --- Metrics ---

def test_evaluate_metrics_diversity():
    songs = [
        make_song(1, "pop", "happy", 0.8, artist="A"),
        make_song(2, "lofi", "chill", 0.4, artist="B"),
        make_song(3, "rock", "intense", 0.9, artist="C"),
        make_song(4, "jazz", "relaxed", 0.5, artist="D"),
        make_song(5, "classical", "melancholy", 0.3, artist="E"),
    ]
    rec = Recommender([])
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    metrics = rec.evaluate_metrics(songs, user)
    assert metrics["genre_diversity"] == 5
    assert metrics["artist_diversity"] == 5
    assert metrics["diversity_score"] == 10

def test_evaluate_metrics_novelty():
    songs = [make_song(i, "pop", "happy", 0.8) for i in range(1, 6)]
    rec = Recommender([])
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    metrics = rec.evaluate_metrics(songs, user, user_history=[1, 2])
    assert metrics["novelty"] == 0.6

def test_evaluate_metrics_novelty_none_without_history():
    songs = [make_song(i, "pop", "happy", 0.8) for i in range(1, 6)]
    rec = Recommender([])
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    metrics = rec.evaluate_metrics(songs, user)
    assert metrics["novelty"] is None

# --- Scoring edge cases ---

def test_genre_match_scores_higher_than_mood_only():
    genre_match = make_song(1, "pop", "sad", 0.5)
    mood_match = make_song(2, "rock", "happy", 0.5)
    rec = Recommender([genre_match, mood_match])
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.5, likes_acoustic=False)
    results = rec.recommend(user, k=2)
    assert results[0].genre == "pop"

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
