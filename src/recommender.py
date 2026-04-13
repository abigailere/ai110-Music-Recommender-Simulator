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


def score_wildcard(song: Dict, target_mood: str, target_energy: float, target_valence: float) -> Tuple[float, str]:
    """
    Scores a song using a valence-first formula.
    Valence (0.45) and danceability (0.30) drive the result;
    mood (0.15) and energy (0.10) are still considered but secondary.
    """
    mood_adjacency = {
        "happy": "relaxed", "relaxed": "happy",
        "chill": "focused", "focused": "chill",
        "intense": "moody", "moody": "intense",
    }

    # Valence proximity (weight 0.45) — primary driver
    valence_score = 1.0 - abs(target_valence - song["valence"])
    if valence_score >= 0.85:
        valence_reason = f"valence is a strong match ({song['valence']} vs target {target_valence})"
    else:
        valence_reason = f"valence ({song['valence']}) near target {target_valence}"

    # Danceability (weight 0.30) — secondary driver, raw score, higher is better
    dance_score = song["danceability"]
    if dance_score >= 0.75:
        dance_reason = f"high danceability ({dance_score})"
    else:
        dance_reason = f"danceability {dance_score}"

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
    Returns a single wildcard song scored by valence and danceability.
    Excludes songs already in the regular recommendations so the pick is always fresh.
    """
    exclude_titles = {s["title"] for s in (exclude or [])}
    candidates = [s for s in songs if s["title"] not in exclude_titles]

    scored = [
        (song, *score_wildcard(song, user_prefs["favorite_mood"], user_prefs["target_energy"], user_prefs["target_valence"]))
        for song in candidates
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0]


def score_song_by_vibe(song: Dict, target_mood: str, target_energy: float) -> Tuple[float, str]:
    """
    PSEUDOCODE version — works on plain dicts instead of Song objects,
    and returns an explanation string alongside the score.
    Compare against score_song_by_vibe() above.

    PSEUDOCODE:
    ---
    FUNCTION score_song_by_vibe_v2(song, target_mood, target_energy):

        # --- Rule 1: Mood Match (weight 0.45) ---
        DEFINE mood_adjacency:
            "happy"   -> "relaxed"
            "relaxed" -> "happy"
            "chill"   -> "focused"
            "focused" -> "chill"
            "intense" -> "moody"
            "moody"   -> "intense"

        IF song["mood"] == target_mood:
            mood_score = 1.0
            mood_reason = "exact mood match ({target_mood})"
        ELSE IF mood_adjacency[target_mood] == song["mood"]:
            mood_score = 0.5
            mood_reason = "adjacent mood ({song['mood']} ~ {target_mood})"
        ELSE:
            mood_score = 0.0
            mood_reason = "mood mismatch"

        # --- Rule 2: Energy Proximity (weight 0.40) ---
        energy_score = 1.0 - abs(target_energy - song["energy"])
        IF energy_score > 0.8:
            energy_reason = "energy close ({song['energy']} vs target {target_energy})"
        ELSE:
            energy_reason = "energy off ({song['energy']} vs target {target_energy})"

        # --- Rule 3: Valence Alignment (bonus +0.1) ---
        IF target_mood in ["happy", "relaxed"] AND song["valence"] > 0.7:
            valence_bonus = 0.1
            valence_reason = "high valence fits positive mood"
        ELSE IF target_mood in ["moody", "intense"] AND song["valence"] < 0.6:
            valence_bonus = 0.1
            valence_reason = "low valence fits dark mood"
        ELSE:
            valence_bonus = 0.0
            valence_reason = ""

        # --- Rule 4: Danceability Boost (bonus up to +0.1) ---
        IF target_energy > 0.7:
            danceability_bonus = song["danceability"] * 0.1
        ELSE:
            danceability_bonus = 0.0

        # --- Final Score ---
        score = (mood_score * 0.45) + (energy_score * 0.40) + valence_bonus + danceability_bonus

        # --- Build explanation ---
        reasons = [mood_reason, energy_reason]
        IF valence_reason != "": APPEND valence_reason to reasons
        explanation = JOIN reasons WITH ", "

        RETURN (score, explanation)
    ---
    """
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
