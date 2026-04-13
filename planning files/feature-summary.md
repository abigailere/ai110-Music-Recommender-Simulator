# Content-Based Recommender — Feature Summary

Based on `data/songs.csv` (10 songs, 10 columns)

---

## Most Effective Features

These five form the recommended feature vector for computing song similarity:

```
[energy, tempo_bpm, valence, danceability, mood (one-hot encoded)]
```

| Feature | Type | Range in Dataset | Why It Works |
|---|---|---|---|
| **energy** | Numeric | 0.28 – 0.93 | Widest spread; clearest separator between calm and intense songs |
| **tempo_bpm** | Numeric | 60 – 152 | Wide range; adds signal independent of energy |
| **valence** | Numeric | 0.48 – 0.84 | Captures emotional positivity; separates moody from happy independent of energy |
| **danceability** | Numeric | 0.41 – 0.88 | Decent spread; useful supporting signal alongside energy |
| **mood** | Categorical | 6 values | Maps directly to user intent; one-hot encode before use |

> Normalize all numeric features to a 0–1 scale, then use **cosine similarity** to find the closest songs.

---

## Least Effective Features

These are either non-numeric, redundant, or too clustered in the current dataset to add meaningful separation:


| Feature | Type | Issue |
|---|---|---|
| **acousticness** | Numeric | Clusters by genre — lofi/ambient/jazz all score 0.71–0.92, others 0.05–0.35. Adds little beyond what `genre` already captures |
| **genre** | Categorical | Useful as a hard filter or soft boost, but not ideal inside a similarity vector |
| **title** | Text | Not usable for similarity math |
| **artist** | Text | Not a content feature; better used as a separate "more from this artist" rule |

> These features are not useless — `genre` works well as a pre-filter before running similarity, and `artist` can be a tie-breaker — they just shouldn't be in the core feature vector.

---

## Practical Recommendations for Your Recommender

## Vibe-Based Scoring Rules

For a playlist builder focused on **mood and energy**, use a weighted scoring system instead of cosine similarity.

### Score Formula

```
score = (mood_score × 0.45) + (energy_score × 0.40) + valence_bonus + danceability_bonus
```

### Rule 1: Mood Match (weight: 0.45)

Mood is categorical — use adjacency instead of binary match/no-match:

| Match type | Score |
|---|---|
| Exact match | 1.0 |
| Adjacent mood | 0.5 |
| No match | 0.0 |

Mood adjacency map:
- `happy` ↔ `relaxed` (both positive, different energy)
- `chill` ↔ `focused` (both low-energy, calm)
- `intense` ↔ `moody` (both high-stakes, darker tone)

### Rule 2: Energy Proximity (weight: 0.40)

```
energy_score = 1.0 - abs(target_energy - song.energy)
```

### Rule 3: Valence Alignment (bonus: +0.1)

Valence reinforces the emotional tone of the mood:

| Mood | Preferred valence |
|---|---|
| happy, relaxed | high (> 0.7) → +0.1 bonus |
| moody, intense | low (< 0.6) → +0.1 bonus |
| chill, focused | neutral — no bonus applied |

### Rule 4: Danceability Boost (bonus: up to +0.1)

Only applied when target energy is high — irrelevant for calm vibes:

```
if target_energy > 0.7:
    danceability_bonus = song.danceability × 0.1
else:
    danceability_bonus = 0
```

### Explainability

For each returned song, generate a reason string based on which rules fired. Maps to `explain_recommendation()` in `recommender.py`.
