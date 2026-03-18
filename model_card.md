# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

- GrooveMatch

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration 

- GrooveMatch is designed to generate a ranked list of song recommendations from a fixed catalog based on a user's stated genre preference, mood preference, and desired energy level. The model assumes each user has exactly one favorite genre, one favorite mood, and a single numeric energy target with other factors (listening history, implicit feedback, or sense of how preferences change over time).

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

- Every song in the catalog gets a score based on how well it matches your preference. First, if the song's genre matches your favorite genre, it gets a big bonus. Then, if the mood also matches, it gets a smaller bonus. Finally, the system looks at how close the song's energy level is to your target (the closer it is, the more points it earns). All three numbers are added together into a final score, and the songs with the highest scores are returned as your recommendations. 

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

- The catalog contains 19 songs across 14 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, hip-hop, country, metal, r&b, folk, blues, and electronic. Moods represented include happy, chill, intense, relaxed, moody, focused, melancholy, energetic, nostalgic, romantic, and dreamy. No songs were removed, but several songs were added to the original dataset to cover more genres and edge cases. Several moods like "sad" or "angry" have no songs at all, so a user with those preferences will never get a match. 

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition 

- The system worked well for users whose favorite genre is well-represented in the catalog. The scoring also handles the standard profiles (pop fan, chill listener, workout listener) intuitively, as it shows the top result in each case is a song that a person with those tastes would enjoy. The explanation output makes it easier to trace exactly why a song ranked where it did. 

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

- The scoring formula awards a fixed +2.0 bonus for a genre match, which is equal to the maximum combined score of mood and energy together. This makes genre the single most decisive factor in every recommendation, as a song in the user's preferred genre will almost always rank above a better-fitting song from a different genre. Combined with an unequal dataset where some genres have only one song, users who favor underrepresented genres receive fewer quality candidates and fall back to pure energy ranking. The system also has no diversity mechanism and the top "k" results are within the same genre, which reinforces what a user likes instead of recommended different music.
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

- I tested three standard profiles (pop fan, chill listener, and workout listener) and six edge cases designed to stress-test the scoring (energy value outside the normal range, nonexistent mood, nonexistent genre, conflicting preferences, ignoring acousticness, and tiebreakers) 

- For recommendations, I checked if the top result actually made sense for the stated preferences and if the score explanation correctly showed which factors contributed. I also checked if any profiles produced unexpected winners. 

- The biggest surprise was how much the genre bonus controls the outcome, as a song that matched the user's genre always ranked near the top even if the mood and energy were a poor fit. I also realized that the acousticness has no effect on results at all, and entering "sad" as a mood preference failed silently since it's not a recognized mood. 

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

- I would reduce the genre bonus or make it proportional so mood and energy have more influence on the total score. I would implement a diversity pass so the top "k" results span more than one genre. I would expand the catalog to cover underrepresented genres and moods. I would also incorporate acousticness into the final score to accomodate for users who prefer acoustic or non-acoustic songs. 

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

- Through this recommender, I learned that a simple recommender like this has real design decisions with real consequences. The choice to weigh genre at twice the value of mood wasn't obvious until the results showed the heavy bias genre had towards the total score of a song. On paper it looked reasonable for what the recommender was supposed to model, but it causes the recommender to not show songs outside of a user's "comfort zone". The gap between efficieny on paper versus the actual output shows why the music apps like Spotify or Apple Music invest a lot towards tuning recommendations. It's also altered my view on recommendations on these music apps, as there's a complex formula scoring that accounts for just more than recommended songs to user's based on genre. 
