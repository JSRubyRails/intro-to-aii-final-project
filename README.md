# GrooveMatch — AI Music Recommender

## Original Project

This project extends the **Explain-an-AI Simulation (Module 3)** music recommender starter. The original goal was to build a rule-based song recommender that scores a catalog of songs against a user's stated preferences (genre, mood, and energy level), return the top 5 matches, and explain why each song ranked where it did. It was designed for classroom exploration of how simple scoring formulas mirror real-world AI recommenders and where bias can emerge from design decisions.

---

## Title and Summary

**GrooveMatch** is a music recommender system that scores songs from a 34-song catalog against a user profile, detects genre bias in the results, and automatically re-ranks recommendations to improve diversity. It uses the Gemini API (gemma-3-1b-it) to generate natural-language explanations for each recommendation and a plain-English summary of any bias correction that occurred. The project demonstrates an agentic workflow — the system plans, acts, checks its own output, and corrects itself without human intervention.

---

## Architecture Overview

The system is organized into five stages:

1. **Recommender** — scores all songs using an additive formula (genre match +2.0, mood match +1.0, energy similarity +0–1.0) and returns the top-5.
2. **Agentic Critique Loop** — runs `detect_bias()` on the results. If any genre appears in 4+ of 5 slots (>70%), it re-ranks using a hard genre cap (max 2 songs per genre) and logs which songs were swapped.
3. **Gemini API** — calls `ai_explain()` to generate a one-sentence explanation per song and `ai_critique_summary()` to narrate the bias correction.
4. **Evaluator** — computes genre diversity, artist diversity, overall diversity score, and novelty (fraction of recommendations the user hasn't heard before).
5. **Human / Testing Checkpoint** — the swap log, bias report, and metrics are printed for human review. `tests/test_recommender.py` validates the scoring logic (reference system_diagram.png for the system diagram).

---

## Setup Instructions

1. Clone the repository and navigate into the project folder:

```bash
cd intro-to-aii-final-project
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate      # Mac / Linux
.venv\Scripts\activate         # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create your `.env` file from the example and add your Gemini API key:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your key from [aistudio.google.com](https://aistudio.google.com):

```
GOOGLE_API_KEY=your-key-here
```

5. Run the recommender:

```bash
python3 src/main.py
```

6. Run tests:

```bash
pytest
```

---

## Sample Interactions

### Example 1 — No Bias Detected (Pop Fan)

**Input:**
```
favorite_genre: pop | favorite_mood: happy | target_energy: 0.8 | likes_acoustic: False
user_history: [1, 5, 10]
```

**Output:**
```
#1  City Lights by Neon Echo
    Why: “City Lights” by Neon Echo’s upbeat pop sound and energetic vibe perfectly align with a listener seeking a joyful and uplifting experience with a moderate energy level (0.8).

#2  Sunrise City by Neon Echo
    Why: Sunrise City perfectly suits a listener who enjoys upbeat pop music with a bright, energetic vibe and a mood that’s inherently cheerful and optimistic.

#3  Gym Hero by Max Pulse
    Why: “Gym Hero” by Max Pulse’s energetic pop sound and uplifting vibe perfectly aligns with a listener who appreciates happy, high-energy music with a moderate intensity (0.8) seeking a feel-good experience.

#4  Rooftop Lights by Indigo Parade
    Why: “Rooftop Lights” by Indigo Parade’s upbeat, shimmering pop sound and energetic vibe perfectly aligns with a listener seeking a joyful and uplifting experience with a moderate tempo and intensity (0.8).

#5  Block Party by Crate Kings
    Why: "Block Party" by Crate Kings’ energetic, upbeat vibe and high energy level perfectly complements a listener who appreciates pop music with a cheerful and optimistic feel, aiming for a mood of 0.8.

  [AI Critique] Here's an explanation of the log:

The music recommender ran a self-critique loop and found no significant bias in its recommendations. It removed several songs – specifically, a few indie pop tracks and a few classic rock songs – because they were deemed to be less frequently listened to by the user base and thus didn’t contribute significantly to the overall diversity of the recommendations. Instead, the removals were replaced with a curated selection of upbeat electronic dance tracks, aiming to increase engagement and introduce users to new genres and artists.
Metrics: {'genre_diversity': 3, 'artist_diversity': 4, 'diversity_score': 7, 'novelty': 0.4}
```

---

### Example 2 — Bias Detected and Corrected (Chill Listener)

**Input:**
```
favorite_genre: lofi | favorite_mood: chill | target_energy: 0.4 | likes_acoustic: True
user_history: [2, 4, 9, 20]
```

**Output:**
```
#1  Rain on Glass by LoRoom
    Why: “Rain on Glass” by LoRoom’s lofi, chill, and energy-focused sound perfectly complements a listener seeking a relaxing and subtly upbeat atmosphere with a low-tempo vibe.

#2  Midnight Coding by LoRoom
    Why: Midnight Coding by LoRoom perfectly fits a listener who appreciates lofi music with a chill vibe and a low energy level (0.4) due to its dreamy, atmospheric soundscape and relaxing, understated feel.

#3  Smoke and Keys by Mellow Brass
    Why: “Smoke and Keys” by Mellow Brass’ chill jazz-influenced lofi track perfectly aligns with a listener seeking a relaxing, low-energy vibe with a focus on subtle, atmospheric soundscapes and a mellow, 0.4 energy level.

#4  Spacewalk Thoughts by Orbit Bloom
    Why: “Spacewalk Thoughts” by Orbit Bloom’s ambient, chill, and energy-low vibe perfectly complements a listener seeking a relaxing, low-tempo lofi track with a gentle, sustained energy level of 0.4.

#5  Coffee Shop Stories by Slow Stereo
    Why: “Coffee Shop Stories” by Slow Stereo’s jazz-infused lofi tracks with a relaxed tempo and low energy perfectly complement a listener seeking a chill, atmospheric experience with a subtle, consistent vibe.

  [AI Critique] The music recommender identified a strong bias towards the genre "lofi" and the artist "LoRoom," leading to a disproportionate representation of this style.  The system subsequently removed songs with a similar vibe – specifically, "LoRoom" – and replaced them with songs that offer a broader range of moods and styles, including tracks with a slightly more upbeat feel and a focus on "chill" music, aiming for a more diverse and engaging recommendation experience.
  [Swap] Removed 'Late Night Study' (lofi, chill) → Added 'Smoke and Keys' (jazz, chill) to reduce lofi dominance
  [Swap] Removed 'Foggy Morning' (lofi, chill) → Added 'Spacewalk Thoughts' (ambient, chill) to reduce lofi dominance
  [Swap] Removed 'Library Rain' (lofi, chill) → Added 'Coffee Shop Stories' (jazz, relaxed) to reduce lofi dominance
Metrics: {'genre_diversity': 3, 'artist_diversity': 4, 'diversity_score': 7, 'novelty': 0.8}
```

---

## Design Decisions

**Why genre is worth +2.0:**
Genre was weighted highest because it is the strongest signal of whether a user will enjoy a song. A pop listener rarely wants a metal recommendation regardless of energy match. The tradeoff is that genre dominates the score — a genre-matched song with the wrong mood will almost always outscore a better overall fit from a different genre.

**Why the agentic re-rank uses a hard genre cap instead of a penalty:**
An early version penalized over-represented genres by subtracting points. This failed for profiles with strong genre dominance (like jazz or lofi) because the genre bonus (+2.0) was too large to overcome with a small penalty. A hard cap of 2 songs per genre guarantees diversity regardless of score spread.

**Why the Gemini API is used for explanations instead of rule-based strings:**
Rule-based explanations produce the same formulaic output every time. The Gemini API generates natural-language explanations that vary per song and feel more like something a real app would show a user. The tradeoff is rate limits and latency — a 2-second delay is added between calls to stay under the free-tier quota of 30 requests/minute.

**Why novelty requires a user history list:**
Novelty is only meaningful relative to what a specific user has already heard. Rather than hardcoding a shared history, each profile carries its own `history` list of previously heard song IDs so novelty scores are personalized.

---

## Testing Summary

**What worked:**
- Standard profiles (Pop Fan, Chill Listener, Workout Mode) produced sensible top-5 results where the top song always matched both genre and mood.
- The agentic critique loop correctly detected and resolved bias for all three biased profiles (Chill Listener, Workout Mode, Jazz Adventurer).
- Novelty scores correctly reflected each profile's listening history.

**What didn't work initially:**
- The penalty-based re-ranking failed for jazz and lofi profiles because the +2.0 genre bonus was too large to overcome. Switching to a hard genre cap fixed this.
- The Gemini model (gemma-3-1b-it) hallucinated song names in the critique summary when asked to name specific swapped songs. The fix was to print swap details directly from the structured log and only use the AI for the high-level bias narrative.
- The free-tier quota for gemini-2.0-flash was 0 requests, requiring a switch to gemma-3-1b-it.

**What I learned:**
Bias in the results was a direct consequence of a design decision (genre weight = 2.0) that looked reasonable on paper. The system needed an explicit correction mechanism — detecting the problem wasn't enough.

---

## Reflection

Building GrooveMatch showed me that a recommender is just a number produced by a formula, and every design choice about what to weight and how much becomes a statement about whose taste matters. Giving genre a 2.0 bonus seemed intuitive, but it caused the system to reinforce what a user already listens to rather than surfacing anything new — which is exactly the criticism people level at real apps like Spotify.

The most useful thing I added was the agentic critique loop. Having the system detect its own bias and correct it without human input changed the project from a passive scorer into something that can actually check its work. That loop — plan, act, evaluate, correct — is the same pattern used in more advanced AI agents, just applied to a simple music list. It made the system more honest about its own limitations.


**Testing**
10 out of 10 tests passed. Tests cover four areas: scoring correctness (genre-matched songs always rank above mood-only matches), bias detection (correctly flags when one genre dominates >70% of results and passes diverse lists), the agentic critique loop (verified that bias is resolved after re-ranking and that no re-rank occurs when results are already diverse), and evaluation metrics (genre diversity, artist diversity, and novelty all return correct values). The only reliability issue encountered was with the Gemini API critique summary — the small gemma-3-1b-it model occasionally hallucinated song names, which was fixed by printing swap details directly from the structured log instead of relying on the AI to extract them.




**What are the limitations or biases in your system?**
Genre is weighted at +2.0 points — twice the value of mood — which means a genre-matched song almost always outranks a better overall fit from a different genre. The catalog is also uneven: genres like lofi have 7 songs while others have only 1, so users with niche preferences get weaker candidates. Moods and genres not in the catalog (like "sad" or "k-pop") fail silently with no warning to the user.



**Could your AI be misused, and how would you prevent that?**
The Gemini API narrates bias corrections in plain English, but the small model (gemma-3-1b-it) sometimes invents song names or genres that don't exist in the results. If someone relied on the AI narrative as ground truth rather than the structured log, they'd get misinformation. The fix is what we already did — use the AI only for high-level summaries and print factual swap details directly from the code.



**What surprised you while testing your AI's reliability?**
The penalty-based re-ranking approach failed completely for profiles with strong genre dominance. Even after subtracting penalty points, jazz and lofi songs still outscore everything else because the +2.0 genre bonus is too large to overcome with a small deduction. Switching to a hard genre cap (max 2 per genre) was the only approach that actually guaranteed bias resolution every time.



**Collaboration with AI during this project:**
One helpful instance: Claude suggested switching from a penalty-based re-ranking to a hard genre cap, which immediately fixed the bias resolution failures that the penalty approach couldn't handle. One flawed instance: Claude initially suggested using google.generativeai as the package for Gemini integration, which turned out to be deprecated — the correct package is google-genai, and the model name gemini-1.5-flash wasn't accessible on the free tier either, requiring multiple corrections before it worked.