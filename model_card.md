# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name : Vinyl Vibes (RAG Music Recommender)

<!-- Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

--- -->

## 2. Intended Use  

<!-- Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

--- -->

This model is supposed to recommend songs to user based on their preferences. It assumes that
energy is the most important weight, and after that acousticness. This currently is designed for real users, which is why it will be hosted on Streamlit. 


## 3. How the Model Works  

<!-- Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program. -->

The datasets features include: id, title, artist, genre, mood, energy, tempo_bpm, valence,danceability, and acousticness. In a more real setting, I would need to use all the features and incorporate in a way of least bias. However, features with the weights used for this model are :
    weights = {
        "energy":       0.30,
        "acousticness": 0.25,
        "tempo":        0.20,
        "mood":         0.15,
        "genre":        0.10,
    }

Changes I made from the starter logic is, at first I had the user profiles as a dictionary within a dictionary and they all ran like a pytest. The terminal would say the tests passed, but it was useless for me. I had to change the code and make it in a way I can run one profile at a time. 

## 4. Data  

<!-- Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

--- -->

There are 50 songs in the catalog. The genres represented are pop, lofi, rock, jazz, synthwave, indie pop, blues, hip-hop, country, r&b, metal, folk, electronic, classical, latin, and ambient. The songs listed can be broken up into more detailed categories like kpop for BTS. There are definitely parts of musical taste missing in this dataset because so many genres are not included like bollywood and rap. 


## 5. Strengths  

<!-- Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

--- -->

The system works for basic music listeners. It gives reasonable results for pop music and casual listeners. The recommendations the model gave for all the user profiles created were successful. 


## 6. Limitations and Bias 

<!-- Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

--- -->

Claude helped me find weights that are the least biased as possible. However, there is still a lot of bias. According to Claude danceability should not be considered as a weight. As a trained dancer, songs danceability is important to me. So this model favors users who are not dancers and may not like to dance at all. The original weight I am using is:
    weights = {
        "energy":       0.30,
        "acousticness": 0.25,
        "tempo":        0.20,
        "mood":         0.15,
        "genre":        0.10,
    }
I doubled energy and halved genre to see the change in recommendations. The only slight change I noticed was in acousticness. This new weight is incorrect either way because it doesnt add up to 1. Also, giving too much value to energy is a biased approach because giving too much weight to one field makes it biased. 
    weights = {
         "energy":       0.60,
         "acousticness": 0.25,
         "tempo":        0.20,
         "mood":         0.15,
         "genre":        0.05,
     }

There is no confidence scoring implemented currently. That will be part of future work. 

## 7. Evaluation  

<!-- How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some. -->

---
<!-- The user profiles I tested are "amateur dancer", "chill listener", "workout fan" and "late night". I looked to see if the recommendations seemed reasonable. The top recommendations for each profile was different. The amateur profile recommended "Hips Don't Lie" by Shakira, which I think is the right recommendation. The workout fan got "Neon Pulse", which is also correct because someone who uses the song for working out would need something upbeat.  -->
Guardrails Implemented:
- Error handling guardrails (agent.py — _call_gemini())

429 → quota exceeded message
401/403 → invalid API key message
404 → model not found message
Client closed → resets the client and prompts retry

- Profile validation guardrail (chat.py and app.py)

If Gemini returns something that isn't a valid profile key, the app catches it and skips instead of crashing

- Hallucination guardrail (agent.py — format_response prompt)

The prompt explicitly tells Gemini: "Do not add any songs that are not in the list above" — prevents Gemini from inventing songs outside your CSV results

## 8. Future Work  

<!-- Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

--- -->

Currently, a csv of songs is stored under 'data/songs.csv'. My future goals of this application is to either incorporate Spotify API for songs or use a vector database of songs. 

## 9. Personal Reflection  

<!-- A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps   -->

I learned the importance of guardrails from this project. I hope to add more guardrails in the project and future projects. I also learned how it is easy to release an application without thinking of the harm it can cause without guardrails. 

<!-- There can be a lot of bias if you incorporate weights incorrectly. It has changed the way I think about the Data professionals who work in music streaming corporations because they will be working with extremely huge list of features and complex weights which change from time to time to recommend new songs.  -->
