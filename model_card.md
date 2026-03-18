# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
