import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

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
    favorite_mood: str
    target_energy: float
    target_valence: float # the most independent signal you're not capturing, and it would let users express "I want dark/moody" vs "I want uplifting" directly
    target_acoustic: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = sorted(
            self.songs,
            key=lambda song: score_song_by_vibe(asdict(song), user.favorite_mood, user.target_energy)[0],
            reverse=True
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a score breakdown and a plain-English reason why a song was recommended."""
        # should give an exaplanation defined by the output data and another one explained in plain english
        score, data_explanation = score_song_by_vibe(asdict(song), user.favorite_mood, user.target_energy)

        mood_adjacency = {
            "happy": "relaxed", "relaxed": "happy",
            "chill": "focused", "focused": "chill",
            "intense": "moody", "moody": "intense",
        }

        if song.mood == user.favorite_mood:
            mood_line = f"its mood is a perfect match for {user.favorite_mood}"
        elif mood_adjacency.get(user.favorite_mood) == song.mood:
            mood_line = f"its {song.mood} vibe is close to your {user.favorite_mood} preference"
        else:
            mood_line = f"its mood ({song.mood}) doesn't quite match your {user.favorite_mood} preference"

        energy_diff = abs(user.target_energy - song.energy)
        if energy_diff <= 0.1:
            energy_line = "the energy level is right on target"
        elif energy_diff <= 0.2:
            energy_line = "the energy level is close to what you want"
        else:
            energy_line = f"the energy ({song.energy:.2f}) is a bit off from your target ({user.target_energy:.2f})"

        plain = f'"{song.title}" by {song.artist} — {mood_line}, and {energy_line}.'

        return f"Score: {score:.2f}\nData: {data_explanation}\nWhy: {plain}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    numeric_fields = {"id": int, "energy": float, "tempo_bpm": float,
                      "valence": float, "danceability": float, "acousticness": float}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field, cast in numeric_fields.items():
                row[field] = cast(row[field])
            songs.append(row)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, *score_song_by_vibe(song, user_prefs["favorite_mood"], user_prefs["target_energy"]))
        for song in songs
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


def score_wildcard(song: Dict, target_mood: str, target_energy: float) -> Tuple[float, str]:
    """Scores a song by valence and danceability derived from mood and energy, with mood and energy as tiebreakers."""
    mood_to_valence = {
        "happy":   0.82,
        "relaxed": 0.70,
        "chill":   0.60,
        "focused": 0.55,
        "moody":   0.42,
        "intense": 0.50,
    }
    target_valence = mood_to_valence.get(target_mood, 0.60)
    target_danceability = 0.4 + (target_energy * 0.5)

    mood_adjacency = {
        "happy": "relaxed", "relaxed": "happy",
        "chill": "focused", "focused": "chill",
        "intense": "moody", "moody": "intense",
    }

    # Valence proximity (weight 0.45) — primary driver
    valence_score = 1.0 - abs(target_valence - song["valence"])
    if valence_score >= 0.85:
        valence_reason = f"valence is a strong match ({song['valence']} vs target {target_valence:.2f})"
    else:
        valence_reason = f"valence ({song['valence']}) near target {target_valence:.2f}"

    # Danceability proximity (weight 0.30) — secondary driver
    dance_score = 1.0 - abs(target_danceability - song["danceability"])
    if dance_score >= 0.85:
        dance_reason = f"danceability is a strong match ({song['danceability']} vs target {target_danceability:.2f})"
    else:
        dance_reason = f"danceability ({song['danceability']}) near target {target_danceability:.2f}"

    # Mood match (weight 0.15)
    if song["mood"] == target_mood:
        mood_score = 1.0
        mood_reason = f"mood matches ({target_mood})"
    elif mood_adjacency.get(target_mood) == song["mood"]:
        mood_score = 0.5
        mood_reason = f"adjacent mood ({song['mood']} ~ {target_mood})"
    else:
        mood_score = 0.0
        mood_reason = f"different mood ({song['mood']})"

    # Energy proximity (weight 0.10)
    energy_score = 1.0 - abs(target_energy - song["energy"])

    score = (valence_score * 0.45) + (dance_score * 0.30) + (mood_score * 0.15) + (energy_score * 0.10)
    explanation = ", ".join([valence_reason, dance_reason, mood_reason])

    return (score, explanation)


def recommend_wildcard(user_prefs: Dict, songs: List[Dict], exclude: Optional[List[Dict]] = None) -> Tuple[Dict, float, str]:
    """
    Returns a single wildcard song scored by valence and danceability. Excludes songs already in the regular recommendations so the pick is always fresh.
    """
    exclude_titles = {s["title"] for s in (exclude or [])}
    candidates = [s for s in songs if s["title"] not in exclude_titles]

    scored: List[Tuple[Dict, float, str]] = []
    for song in candidates:
        score, explanation = score_wildcard(song, user_prefs["favorite_mood"], user_prefs["target_energy"])
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0]


def score_song_by_vibe(song: Dict, target_mood: str, target_energy: float) -> Tuple[float, str]:
    """Scores a song against a user's mood and energy using weighted rules for mood, energy, valence, and danceability."""
    # Rule 1: Mood Match (weight 0.45)
    mood_adjacency = {
        "happy": "relaxed",
        "relaxed": "happy",
        "chill": "focused",
        "focused": "chill",
        "intense": "moody",
        "moody": "intense",
    }

    if song["mood"] == target_mood:
        mood_score = 1.0
        mood_reason = f"exact mood match ({target_mood})"
    elif mood_adjacency.get(target_mood) == song["mood"]:
        mood_score = 0.5
        mood_reason = f"adjacent mood ({song['mood']} ~ {target_mood})"
    else:
        mood_score = 0.0
        mood_reason = "mood mismatch"

    # Rule 2: Energy Proximity (weight 0.40)
    energy_score = 1.0 - abs(target_energy - song["energy"])
    if energy_score > 0.8:
        energy_reason = f"energy close ({song['energy']} vs target {target_energy})"
    else:
        energy_reason = f"energy off ({song['energy']} vs target {target_energy})"

    # Rule 3: Valence Alignment (bonus +0.1)
    if target_mood in ("happy", "relaxed") and song["valence"] > 0.7:
        valence_bonus = 0.1
        valence_reason = "high valence fits positive mood"
    elif target_mood in ("moody", "intense") and song["valence"] < 0.6:
        valence_bonus = 0.1
        valence_reason = "low valence fits dark mood"
    else:
        valence_bonus = 0.0
        valence_reason = ""

    # Rule 4: Danceability Boost (bonus up to +0.1)
    if target_energy > 0.7:
        danceability_bonus = song["danceability"] * 0.1
    else:
        danceability_bonus = 0.0

    # Final Score
    score = (mood_score * 0.45) + (energy_score * 0.40) + valence_bonus + danceability_bonus

    # Build explanation
    reasons = [mood_reason, energy_reason]
    if valence_reason:
        reasons.append(valence_reason)
    explanation = ", ".join(reasons)

    return (score, explanation)
