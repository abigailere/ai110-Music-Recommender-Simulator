# How Streaming Platforms Predict What You'll Love

---

## Collaborative Filtering — "People Like You"

Ignores what a song *sounds like* and focuses on **patterns of human behavior**.

**How it works:**
- Builds a massive matrix: users on one axis, songs on the other, with play/skip/like signals as values
- Finds users with similar taste profiles ("user A and user B listen to the same 200 songs")
- Recommends what similar users loved that you haven't heard yet

**Two flavors:**

| Type | Method |
|---|---|
| **User-based** | Find users similar to you, recommend their favorites |
| **Item-based** | Find songs that are co-listened with your favorites |

**Matrix Factorization** (what Spotify actually uses) compresses this into latent vectors — each user and song gets a short numeric embedding. Songs "near" your taste vector get recommended. This powers Spotify's **Discover Weekly**.

- **Strength:** Captures taste that's hard to describe ("I like sad bangers") — no one labels it, but the behavior reveals it
- **Weakness:** Cold start problem — new users with no history get poor recommendations; new songs with no listeners can't be recommended

---

## Content-Based Filtering — "Songs Like This"

Analyzes the **audio and metadata** of songs themselves, not who listens to them.

**What gets extracted:**
- **Audio features:** tempo, key, loudness, danceability, energy, acousticness, speechiness, valence (emotional positivity)
- **Structural features:** song sections, instrumentation, timbre via spectral analysis
- **Metadata:** genre, artist, release year, lyrics sentiment

Spotify's **Echo Nest** (acquired 2014) pioneered assigning every track ~10 numeric audio features. If you play upbeat acoustic folk, the system finds other songs with matching feature vectors.

- **Strength:** Works immediately for new songs (no listening history needed); explainable
- **Weakness:** Can get stuck in a bubble — only recommends things sonically similar

---

## Hybrid Systems — How Platforms Combine Both

No major platform uses just one approach. The real power is in **blending signals**:

```
Final Score = w1 * collaborative_score + w2 * content_score + w3 * context_score
```

**Spotify's approach:**
- Uses **Bandits algorithms** to balance exploration vs. exploitation
- **Session-based context:** what you played in the last 30 minutes influences next recommendations
- **NLP** on blogs, reviews, and playlist titles — if 10,000 playlists called "Late Night Drive" include a song, it learns that context

**YouTube's approach (two-stage neural net):**
1. **Candidate generation:** collaborative filtering narrows 800M videos → ~hundreds of candidates using watch history
2. **Ranking:** a deep neural net scores those candidates using richer features (freshness, click-through rates, watch time, device, time of day)

---

## Other Important Techniques

### Reinforcement Learning
Treats recommendations as a sequential decision problem. Each recommendation is an *action*, and long-term engagement is the *reward*. Prevents over-optimizing for immediate clicks at the cost of user satisfaction.

### Graph Neural Networks
Models the entire ecosystem as a graph: users → playlists → songs → artists. Propagates signals across the graph (a song connected to many "focus music" playlists inherits that context).

### Contextual Signals
- Time of day, day of week
- Device type (phone during commute vs. desktop at work)
- Location (inferred)
- Listening session type (party, sleep, workout)

### Implicit vs. Explicit Feedback

| Signal Type | Example | Weight |
|---|---|---|
| Explicit | Thumbs up/down, saves | High but rare |
| Implicit | Completed listen, repeat play | Medium, very common |
| Negative implicit | Skip in first 10 seconds | Strong negative signal |
- May also take into account if a person is skipping a song alot because they have heard it a lot before = tired of hearing it (measure by how often it was played through before then how many times it was skipped and the gap of time between these two behaviors) (my apporach/note)

---

## The Cold Start Problem & Solutions

| Scenario | Solution |
|---|---|
| New user, no history | Ask onboarding questions, use demographic/location priors |
| New song, no listeners | Content-based features kick in immediately |
| New user who linked social | Bootstrap from social graph connections |

---

## Key Takeaway

Real recommendation systems are **ensemble models**:
- **Collaborative filtering** captures social proof and emergent taste
- **Content-based filtering** captures sonic attributes
- **Contextual models** capture when and why you're listening

The weighting between them shifts dynamically based on how much data the platform has about you and the song.

---

## Main Data Types in Recommendation Systems

### Behavioral Data (What You Do)
| Data Type | Description | Signal Strength |
|---|---|---|
| **Like / Save** | Explicit thumbs up, heart, or save to library | Very high |
| **Skip** | Skipping a song, especially in the first 30 seconds | Strong negative |
| **Skip fatigue** | Song was played many times before, now being skipped — user is tired of it | Medium negative (see note below) |
| **Full listen** | Song played all the way through | Medium positive |
| **Repeat play** | Song played multiple times in a session | High positive |
| **Add to playlist** | User manually added a song to a playlist | High positive |
| **Share** | Song shared with another user or externally | High positive |
| **Search query** | What the user typed to find a song | Intent signal |
| **Queue add** | User manually queued a song next | Medium positive |

> **Skip fatigue note:** A skip after many prior completions is different from a cold skip. Good systems track play-through history vs. skip history and the time gap between them to detect listener burnout rather than dislike.

---

### Audio / Content Data (What the Song Is)
| Data Type | Description | Example Value |
|---|---|---|
| **Tempo (BPM)** | Speed of the track | 128 BPM |
| **Key** | Musical key | C major |
| **Loudness** | Average decibel level | -5 dB |
| **Energy** | Intensity and activity level | 0.87 (0–1 scale) |
| **Danceability** | How suitable for dancing | 0.74 |
| **Valence** | Musical positiveness / mood | 0.3 = sad, 0.9 = happy |
| **Acousticness** | Likelihood the track is acoustic | 0.02 |
| **Speechiness** | Presence of spoken words | 0.05 |
| **Instrumentalness** | Predicts whether a track has no vocals | 0.91 |
| **Liveness** | Presence of a live audience | 0.12 |
| **Duration** | Length of the track | 3:42 |
| **Timbre** | Texture/tone quality of instruments | Vector of values |
| **Genre tags** | Broad or fine-grained genre labels | "indie pop", "lo-fi" |
| **Mood tags** | Human or ML-assigned mood labels | "melancholic", "energetic" |

---

### Social / Graph Data (Who You Are Connected To)
- Followed artists and friends
- Playlists you follow or share
- Co-listening patterns (same songs in many of the same playlists)
- Artist similarity graphs (band A shares members or sound with band B)

### Contextual Data (When and Where)
- Time of day / day of week
- Device type (phone, speaker, desktop)
- Listening session type (workout, sleep, focus)
- Location (country/city level, affects catalog availability and trends)

---

## Platform Comparison: Spotify vs. YouTube Music vs. Apple Music

### Spotify
| Aspect | Detail |
|---|---|
| **Core strength** | Best-in-class music-only recommendation engine |
| **Key feature** | Discover Weekly, Daily Mixes, Radio |
| **Data advantage** | Largest dedicated music listener base; Echo Nest audio analysis on every track |
| **Filtering approach** | Heavy collaborative filtering + NLP on playlists/blogs + audio features |
| **Explicit feedback** | Like (heart), dislike, follow artist |
| **Cold start** | Strong — uses audio features for new tracks immediately |
| **Weakness** | No video context; limited social graph |
| **Unique signal** | Playlist titles analyzed with NLP to assign cultural/mood context to songs |

---

### YouTube Music
| Aspect | Detail |
|---|---|
| **Core strength** | Cross-signal recommendations (music + video + search history) |
| **Key feature** | Auto playlists, "Your Mixtape", music videos + audio versions |
| **Data advantage** | Knows what you watch, search, and listen to across all of YouTube |
| **Filtering approach** | Two-stage neural net (candidate generation → ranking); watch time and engagement heavily weighted |
| **Explicit feedback** | Thumbs up/down |
| **Cold start** | Strong on popular tracks (huge view count data); weaker for niche music |
| **Weakness** | Music recommendations bleed into general YouTube behavior — a watched cooking video can pollute music taste signals |
| **Unique signal** | Video watch time, comment engagement, and search intent all feed into music ranking |

---

### Apple Music
| Aspect | Detail |
|---|---|
| **Core strength** | Human curation + editorial playlists; deep device ecosystem integration |
| **Key feature** | For You, New Music Mix, Friends Mix, Siri suggestions |
| **Data advantage** | Knows your entire iTunes/local library including music you didn't stream; integrates with Siri voice patterns |
| **Filtering approach** | Mix of collaborative filtering and heavy editorial curation; less publicly documented than Spotify |
| **Explicit feedback** | Love (strong), Dislike, Add to Library |
| **Cold start** | Asks for genre preferences at onboarding; imports local library to bootstrap |
| **Weakness** | Less transparent algorithm; recommendation diversity criticized as narrower than Spotify |
| **Unique signal** | Local library listening history (music you own, not just streamed); Siri usage patterns; Apple Watch workout data |

---

### Side-by-Side Summary

| Feature | Spotify | YouTube Music | Apple Music |
|---|---|---|---|
| Algorithm transparency | Medium | Low | Low |
| Human curation | Some | Some | Heavy |
| Audio feature analysis | Very deep (Echo Nest) | Moderate | Moderate |
| Cross-platform signals | Music only | All of YouTube/Google | Apple ecosystem (Siri, Watch) |
| Social features | Friend activity, collaborative playlists | Comments, shares | Friends Mix |
| New artist discovery | Best | Moderate | Moderate |
| Mood/context playlists | Strong | Moderate | Strong (editorial) |
| Podcast/non-music data | Yes (podcasts) | Yes (all video) | Podcasts separate |

Main Data Types — broken into four categories:

Behavioral — likes, skips, repeats, playlist adds, shares, with a note on skip fatigue (your earlier insight is preserved there)
Audio/Content — all the numeric song attributes (tempo, valence, energy, etc.) with example values so it's concrete
Social/Graph — follows, co-listening patterns, artist similarity
Contextual — time, device, location, session type
Platform Comparison — detailed tables for each platform covering their core algorithm approach, unique data advantages, and weaknesses, plus a side-by-side summary at the end. Key differences:

Spotify = deepest audio analysis, best pure music discovery
YouTube Music = broadest cross-signal data (everything you do on YouTube), but music signals can get polluted
Apple Music = leans hardest on human editorial curation and Apple ecosystem signals (Siri, Apple Watch)