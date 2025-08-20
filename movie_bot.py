# movie_bot.py
# A simple CLI Movie Bot — search, recommend, details, and watchlist (no external APIs)
# Run: python movie_bot.py

import json
import os
import re
import difflib
from typing import List, Dict

WATCHLIST_FILE = "watchlist.json"

MOVIES: List[Dict] = [
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genres": ["Drama"],
        "rating": 9.3,
        "cast": ["Tim Robbins", "Morgan Freeman"],
        "plot": "Two imprisoned men bond over years, finding redemption through acts of common decency."
    },
    {
        "title": "The Dark Knight",
        "year": 2008,
        "genres": ["Action", "Crime", "Drama"],
        "rating": 9.0,
        "cast": ["Christian Bale", "Heath Ledger"],
        "plot": "Batman faces the Joker, who plunges Gotham into chaos."
    },
    {
        "title": "Inception",
        "year": 2010,
        "genres": ["Action", "Sci-Fi", "Thriller"],
        "rating": 8.8,
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"],
        "plot": "A thief enters dreams to plant an idea in a CEO's mind."
    },
    {
        "title": "Interstellar",
        "year": 2014,
        "genres": ["Adventure", "Drama", "Sci-Fi"],
        "rating": 8.7,
        "cast": ["Matthew McConaughey", "Anne Hathaway"],
        "plot": "Explorers travel through a wormhole to save humanity."
    },
    {
        "title": "Parasite",
        "year": 2019,
        "genres": ["Comedy", "Drama", "Thriller"],
        "rating": 8.6,
        "cast": ["Song Kang-ho", "Lee Sun-kyun"],
        "plot": "A poor family schemes to infiltrate a wealthy household."
    },
    {
        "title": "Spirited Away",
        "year": 2001,
        "genres": ["Animation", "Adventure", "Family"],
        "rating": 8.6,
        "cast": ["Rumi Hiiragi", "Miyu Irino"],
        "plot": "A girl must save her parents in a spirit world bathhouse."
    },
    {
        "title": "The Godfather",
        "year": 1972,
        "genres": ["Crime", "Drama"],
        "rating": 9.2,
        "cast": ["Marlon Brando", "Al Pacino"],
        "plot": "The aging patriarch of an organized crime dynasty transfers control to his reluctant son."
    },
    {
        "title": "The Matrix",
        "year": 1999,
        "genres": ["Action", "Sci-Fi"],
        "rating": 8.7,
        "cast": ["Keanu Reeves", "Laurence Fishburne"],
        "plot": "A hacker discovers reality is a simulation."
    },
    {
        "title": "Whiplash",
        "year": 2014,
        "genres": ["Drama", "Music"],
        "rating": 8.5,
        "cast": ["Miles Teller", "J.K. Simmons"],
        "plot": "An ambitious drummer faces a ruthless instructor."
    },
    {
        "title": "Coco",
        "year": 2017,
        "genres": ["Animation", "Adventure", "Family", "Music"],
        "rating": 8.4,
        "cast": ["Anthony Gonzalez", "Gael García Bernal"],
        "plot": "A boy enters the Land of the Dead to unlock his family's history."
    },
    {
        "title": "3 Idiots",
        "year": 2009,
        "genres": ["Comedy", "Drama"],
        "rating": 8.4,
        "cast": ["Aamir Khan", "R. Madhavan", "Sharman Joshi"],
        "plot": "Three friends navigate college pressures and chase real learning."
    },
    {
        "title": "KGF: Chapter 1",
        "year": 2018,
        "genres": ["Action", "Drama"],
        "rating": 8.2,
        "cast": ["Yash", "Srinidhi Shetty"],
        "plot": "A young man's rise in the gold mines of Kolar."
    },
    {
        "title": "Baahubali: The Beginning",
        "year": 2015,
        "genres": ["Action", "Drama", "Fantasy"],
        "rating": 8.0,
        "cast": ["Prabhas", "Rana Daggubati", "Anushka Shetty"],
        "plot": "A young man discovers his royal lineage and destiny."
    },
    {
        "title": "Dangal",
        "year": 2016,
        "genres": ["Action", "Biography", "Drama", "Sport"],
        "rating": 8.3,
        "cast": ["Aamir Khan", "Fatima Sana Shaikh"],
        "plot": "A father trains his daughters to become world-class wrestlers."
    },
    {
        "title": "RRR",
        "year": 2022,
        "genres": ["Action", "Drama"],
        "rating": 8.0,
        "cast": ["N.T. Rama Rao Jr.", "Ram Charan"],
        "plot": "Two revolutionaries form a legendary friendship in pre-independent India."
    },
    {
        "title": "Joker",
        "year": 2019,
        "genres": ["Crime", "Drama", "Thriller"],
        "rating": 8.4,
        "cast": ["Joaquin Phoenix", "Robert De Niro"],
        "plot": "A troubled man descends into madness and becomes Joker."
    },
    {
        "title": "Zindagi Na Milegi Dobara",
        "year": 2011,
        "genres": ["Adventure", "Comedy", "Drama"],
        "rating": 8.2,
        "cast": ["Hrithik Roshan", "Farhan Akhtar", "Abhay Deol"],
        "plot": "Three friends rediscover life on a road-trip across Spain."
    },
    {
        "title": "Drishyam",
        "year": 2015,
        "genres": ["Crime", "Drama", "Thriller"],
        "rating": 8.2,
        "cast": ["Ajay Devgn", "Tabu"],
        "plot": "A man goes to extreme lengths to protect his family."
    },
    {
        "title": "Titanic",
        "year": 1997,
        "genres": ["Drama", "Romance"],
        "rating": 7.9,
        "cast": ["Leonardo DiCaprio", "Kate Winslet"],
        "plot": "A romance unfolds aboard the ill-fated RMS Titanic."
    },
    {
        "title": "Your Name",
        "year": 2016,
        "genres": ["Animation", "Drama", "Fantasy", "Romance"],
        "rating": 8.4,
        "cast": ["Ryunosuke Kamiki", "Mone Kamishiraishi"],
        "plot": "Two teenagers mysteriously swap bodies and connect across time."
    },
]

MOOD_TO_GENRES = {
    "happy": ["Comedy", "Family", "Animation", "Adventure", "Music"],
    "sad": ["Drama", "Romance"],
    "thrill": ["Thriller", "Crime"],
    "chill": ["Drama", "Animation"],
    "epic": ["Action", "Adventure", "Fantasy"],
    "mindblown": ["Sci-Fi", "Thriller"],
    "motivation": ["Sport", "Biography", "Drama"]
}

def load_watchlist() -> List[str]:
    if os.path.exists(WATCHLIST_FILE):
        try:
            with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []

def save_watchlist(watchlist: List[str]):
    try:
        with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
            json.dump(watchlist, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[warn] Could not save watchlist: {e}")

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def find_by_title(query: str, n_best: int = 5) -> List[Dict]:
    titles = [m["title"] for m in MOVIES]
    matches = difflib.get_close_matches(query, titles, n=n_best, cutoff=0.4)
    results = []
    for m in MOVIES:
        if m["title"] in matches or normalize(query) in normalize(m["title"]):
            results.append(m)
    return results[:n_best]

def filter_by_genres(genres: List[str]) -> List[Dict]:
    genres_norm = {normalize(g) for g in genres}
    results = []
    for m in MOVIES:
        mg = {normalize(g) for g in m["genres"]}
        if mg & genres_norm:
            results.append(m)
    # Sort by rating desc then year desc
    results.sort(key=lambda x: (x["rating"], x["year"]), reverse=True)
    return results

def filter_by_actor(name: str) -> List[Dict]:
    name_n = normalize(name)
    results = []
    for m in MOVIES:
        if any(name_n in normalize(c) for c in m["cast"]):
            results.append(m)
    results.sort(key=lambda x: (x["rating"], x["year"]), reverse=True)
    return results

def top_rated(limit: int = 5) -> List[Dict]:
    return sorted(MOVIES, key=lambda m: m["rating"], reverse=True)[:limit]

def pretty_movie(m: Dict) -> str:
    return (f"{m['title']} ({m['year']}) — {', '.join(m['genres'])} — ★ {m['rating']}\n"
            f"Cast: {', '.join(m['cast'])}\n"
            f"Plot: {m['plot']}")

HELP_TEXT = """
Commands you can try:
  search <title>            - Find a movie by title
  details <title>           - Show details of a movie
  recommend <genre/mood>    - Get recommendations (e.g., recommend action | recommend happy)
  actor <name>              - Find movies by actor
  top                       - Show top rated picks
  add <title>               - Add a movie to your watchlist
  remove <title>            - Remove from your watchlist
  watchlist                 - Show your watchlist
  help                      - Show this help
  exit                      - Quit the bot
"""

WELCOME = """
🎬  Welcome to MovieBot!
Tell me what you want to watch. Try:
  • search interstellar
  • recommend action
  • recommend happy
  • details joker
  • actor Aamir Khan
  • top
Type 'help' to see all commands.
"""

def handle_search(arg: str):
    if not arg:
        print("Try: search inception")
        return
    results = find_by_title(arg)
    if not results:
        print("No matches found.")
        return
    for i, m in enumerate(results, 1):
        print(f"{i}. {m['title']} ({m['year']}) — ★ {m['rating']} — {', '.join(m['genres'])}")

def handle_details(arg: str):
    if not arg:
        print("Try: details parasite")
        return
    results = find_by_title(arg, n_best=1)
    if not results:
        print("No such movie. Try 'search <title>'")
        return
    print(pretty_movie(results[0]))

def handle_recommend(arg: str):
    if not arg:
        print("Try: recommend action | recommend happy")
        return
    key = normalize(arg)
    genres = []
    if key in MOOD_TO_GENRES:
        genres = MOOD_TO_GENRES[key]
    else:
        # accept comma-separated genres
        genres = [g.strip() for g in arg.split(",") if g.strip()]
    results = filter_by_genres(genres)
    if not results:
        print("Couldn't find anything for that. Try a common genre like Action, Drama, Comedy, Sci-Fi.")
        return
    print(f"Recommendations for {', '.join(genres)}:")
    for m in results[:7]:
        print(f"- {m['title']} ({m['year']}) — ★ {m['rating']} — {', '.join(m['genres'])}")

def handle_actor(arg: str):
    if not arg:
        print("Try: actor Leonardo DiCaprio")
        return
    results = filter_by_actor(arg)
    if not results:
        print("No movies found for that actor.")
        return
    print(f"Movies with {arg}:")
    for m in results[:7]:
        print(f"- {m['title']} ({m['year']}) — ★ {m['rating']} — {', '.join(m['genres'])}")

def handle_top():
    print("Top rated picks:")
    for m in top_rated(7):
        print(f"- {m['title']} ({m['year']}) — ★ {m['rating']} — {', '.join(m['genres'])}")

def handle_add(arg: str, watchlist: List[str]):
    if not arg:
        print("Try: add inception")
        return
    results = find_by_title(arg, n_best=1)
    if not results:
        print("Couldn't find that title.")
        return
    title = results[0]["title"]
    if title in watchlist:
        print(f"'{title}' is already in your watchlist.")
    else:
        watchlist.append(title)
        save_watchlist(watchlist)
        print(f"Added '{title}' to your watchlist.")

def handle_remove(arg: str, watchlist: List[str]):
    if not arg:
        print("Try: remove inception")
        return
    # fuzzy remove
    match = difflib.get_close_matches(arg, watchlist, n=1, cutoff=0.4)
    if match:
        title = match[0]
        watchlist.remove(title)
        save_watchlist(watchlist)
        print(f"Removed '{title}' from your watchlist.")
    else:
        print("That title isn't in your watchlist.")

def handle_watchlist(watchlist: List[str]):
    if not watchlist:
        print("Your watchlist is empty. Try 'add <title>'.")
        return
    print("🎟  Your Watchlist:")
    for i, t in enumerate(watchlist, 1):
        print(f"{i}. {t}")

def parse_command(text: str):
    text = text.strip()
    if not text:
        return ("", "")
    parts = text.split(" ", 1)
    cmd = parts[0].lower()
    arg = parts[1].strip() if len(parts) > 1 else ""
    return (cmd, arg)

def main():
    print(WELCOME)
    print(HELP_TEXT)
    watchlist = load_watchlist()

    while True:
        try:
            user = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! 🍿")
            break

        cmd, arg = parse_command(user)

        if cmd in ("exit", "quit", "q"):
            print("Goodbye! 🍿")
            break
        elif cmd in ("help", "?"):
            print(HELP_TEXT)
        elif cmd == "search":
            handle_search(arg)
        elif cmd == "details":
            handle_details(arg)
        elif cmd == "recommend":
            handle_recommend(arg)
        elif cmd == "actor":
            handle_actor(arg)
        elif cmd == "top":
            handle_top()
        elif cmd == "add":
            handle_add(arg, watchlist)
        elif cmd == "remove":
            handle_remove(arg, watchlist)
        elif cmd == "watchlist":
            handle_watchlist(watchlist)
        else:
            # lightweight intent hints
            low = normalize(user)
            if any(k in low for k in ("recommend", "suggest", "good", "best")):
                # try to extract a genre/mood word
                words = re.findall(r"[a-zA-Z]+", user)
                guess = ""
                for w in words:
                    wlow = w.lower()
                    if wlow in {g.lower() for m in MOVIES for g in m["genres"]} or wlow in MOOD_TO_GENRES:
                        guess = w
                        break
                if guess:
                    handle_recommend(guess)
                else:
                    print("Tell me a genre/mood. Example: recommend action | recommend happy")
            elif "watchlist" in low:
                handle_watchlist(watchlist)
            elif any(k in low for k in ("detail", "plot", "about")):
                # guess title
                results = find_by_title(user, n_best=1)
                if results:
                    print(pretty_movie(results[0]))
                else:
                    print("Try: details <title>")
            else:
                print("I didn't get that. Type 'help' to see commands.")

if _name_ == "_main_":
    main()