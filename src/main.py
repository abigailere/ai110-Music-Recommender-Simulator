from recommender import load_songs, recommend_songs, recommend_wildcard


def display_recommendations(recommendations: list, user_prefs: dict) -> None:
    width = 52
    sep = "-" * width

    print(f"\n{sep}")
    print(f"  User Preference  |  mood: {user_prefs['favorite_mood']}  energy: {user_prefs['target_energy']}")
    print(sep)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        bar_filled = round(score * 20)
        bar = "#" * bar_filled + "." * (20 - bar_filled)
        reasons = [r.strip() for r in explanation.split(",")]

        print(f"\n  #{i}  {song['title']}  -  {song['artist']}")
        print(f"       [{bar}]  {score:.2f}")
        for reason in reasons:
            print(f"       * {reason}")

    print(f"\n{sep}\n")


VALID_MOODS = ["happy", "relaxed", "chill", "focused", "moody", "intense"]


def get_user_prefs() -> dict:
    width = 52
    sep = "-" * width
    print(f"\n{sep}")
    print(f"  Music Recommender")
    print(sep)

    # Mood input
    print(f"\n  Moods: {', '.join(VALID_MOODS)}")
    while True:
        mood = input("  Enter your mood: ").strip().lower()
        if mood in VALID_MOODS:
            break
        print(f"  Invalid mood. Choose from: {', '.join(VALID_MOODS)}")

    # Energy input
    print("\n  Energy is a number from 0.0 (very calm) to 1.0 (very intense)")
    while True:
        raw = input("  Enter your energy level: ").strip()
        try:
            energy = float(raw)
            if 0.0 <= energy <= 1.0:
                break
            print("  Please enter a number between 0.0 and 1.0")
        except ValueError:
            print("  That's not a valid number. Try something like 0.7")

    return {"favorite_mood": mood, "target_energy": energy}


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = get_user_prefs()

    recommendations = recommend_songs(user_prefs, songs, k=5)
    display_recommendations(recommendations, user_prefs)

    wildcard_song, wildcard_score, wildcard_explanation = recommend_wildcard(user_prefs, songs, exclude=[s for s, _, _ in recommendations])
    width = 52
    sep = "-" * width
    bar_filled = round(wildcard_score * 20)
    bar = "#" * bar_filled + "." * (20 - bar_filled)
    reasons = [r.strip() for r in wildcard_explanation.split(",")]
    print(f"{sep}")
    print(f"  Wild Card Pick")
    print(sep)
    print(f"\n  {wildcard_song['title']}  -  {wildcard_song['artist']}")
    print(f"       [{bar}]  {wildcard_score:.2f}")
    for reason in reasons:
        print(f"       * {reason}")
    print(f"\n{sep}\n")


if __name__ == "__main__":
    main()
