# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name: Tap To Resonate

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 
 
- This recommender is perfect for the vibe chaser. This model is for users that to create playlists to fit every mood without limits of genre or artists. Specify a mood and energy level and let the algorithm will suggest 5 songs with a Wild Card as suprise. 
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

- The features I used where dancibility, mood, energy, and valence. I added valence and dancibility as fields and 40 more songs to the dataset. I have the user specify target mood and energy, the main algorithm prioritizes those two field when picking songs with  Mood match counting the most. If a song's mood matches exactly, it gets full points; if it is close but not exact, it gets partial points; if it does not match at all, it gets zero for that part. Energy closeness is the second biggest factor with the closer a song's energy is to what the user specifies, the better it scores. The model also gives small bonus points if the emotional tone of a song (its valence) fits the mood, and if a song is very danceable when in a high-energy mood. All those points are added up, and the five songs with the highest scores are recommended to you. The wild card recommender picks songs that are closer to an assumed dancibility and valence based on the inputed mood and energy. This was added in case a user wants fresh unexpected song. It still takes into account what they originally inputted so that it would make sense but there is a little more freedom with using different fields. That way the suggestions give variety but still fit the overall vibe.

- Changes from starter logic: valence and danceability were added as scoring signals so the emotional tone and rhythm of a song factor into the score, not just mood and energy. Genre was removed from the user profile since this app is vibe-based, not genre-based. The song catalog was also expanded from 4 songs to 50 to give the recommender a more realistic pool to pull from.

---

## 4. Data  

Describe the dataset the model uses.  


- There are a total of 50 songs in the dataset. There are 6 moods, happy, relaxed, intense, moody, chill, and focused so it is mood diverse. The genres are diverse but because the number of data points is small, most genres only have 1-2 songs representing it.
- Lofi is overrepresented with 4 songs meaning that a chill user will likely get a lofi list by default. 
- There is very little classical music

---

## 5. Strengths  

Where does your system seem to work well  


- My system gives the best results for users who have a clear mood and energy in mind. For example, a user who enters "intense" with energy 0.9 will consistently get high-energy songs that match that feeling, because mood and energy together make up 85% of the score. Users in the middle of the mood spectrum — like "moody" or "happy" — also benefit from the adjacency system, which catches songs that are close but not exact matches. 
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

- The most obvious is that it does not consider genres at all. While this is intentional, it can lead to certain genres being unintentionally over suggested because it naturally leans towards a specific mood or energy. Lofi is also over-represented with 4 songs. With 50 datapoints this feels small but because there are so many genres, others do not have the same amount. This leads to a case where if a user wants a chill mood they are almost guaranteed a lofi playlist. Claude also pointed out that the catalog is American centered with very few genres from other parts of the world. The song catalog also skews towards younger listeners by excluding genres like classic rock and classical/orchestral music
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

- I tested predictable user profiles like intense mood with high energy to check that the system worked as expected, returning songs that fit both
- I also tested different energies for the same mood to see if different songs would be suggested which suprisingly did not work as well. It ended up suggesting a lot of the same songs in similar rankings because the energy levels were still close eventhough not exact. This may be an issue with the dataset
- To stretch it, I created user profiles that seemed less intuitive like low energy and intense, which in some cases it behaved as expected (unable to recommend accurately) and sometimes not. Recommendations here were not as accurate since realistically low energy intense songs are not common, which is reflected in my dataset.
- I checked the reasons for each suggestion to check whether the weights I wrote in my algorithm produced results that made sense.
---

## 8. Future Work  

Ideas for how you would improve the model next.  
 
- If I were to improve this model with more time, I would add the ability to save recommended songs or add a little randomness so that a user would not get the exact same songs when inputting the same data everytime the program is run. This would make it more reflective of a real recommendation algorithm
-  I would also expand the dataset so that there is more diversity in types of moods and energy within a single genre. It would be less likely to produce a situation where chill mood = lofi genre
---

## 9. Personal Reflection  

A few sentences about your experience.  

- I learned that building a recommendation system takes a lot of planning. It requires thinking about what a user is expecting when they give their preferences. I did not expect it to require so much data to be accurate. I created 50 data points but that may not be enough to get a good working system. In a way it confirmed
- I use Spotify and one of things I love about the platform is its diverse playlists and ability to recommend diverse songs, however my biggest issue is that once it figures out what you like, it is hard to get recommendations outside of what it has assessed. Building my recommender helped shed light on how difficult it is to balance what users specify as their tastes and how a person actually interacts with music. 
