#Ayden Hayes
#12/12/24
#find_subs.py 
# second test to find spanish speaking subreddits
import praw
import json
import time
from langdetect.lang_detect_exception import LangDetectException
from prawcore.exceptions import RequestException, TooManyRequests, Forbidden
from langdetect import detect
from reddit_config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

#----------------------#
# SETTINGS:
NUM_POSTS = 100  # Posts per subreddit
OUTPUT_FILE = "./subreddits_by_keyword.json"
MAX_RETRIES = 5
MIN_MEMBERS = 10000 # only save subreddits with this many members
#----------------------#

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def is_spanish(text):
    try:
        language = detect(text)
        return language == 'es'
    except (LangDetectException, TypeError):
        return False

def is_spanish_subreddit(subreddit, check_limit=10, required_percent=0.5):
    if is_spanish(subreddit.public_description):
        return True
    #TODO: me when python
    try:
        count_spanish = sum(
            1 for post in subreddit.top(limit=check_limit)
            if is_spanish(post.title + " " + post.selftext)
        )
        return count_spanish / check_limit >= required_percent
    except Exception as e:
        return False

#TODO: lmao?
def fetch_with_retries(func, *args, retries=MAX_RETRIES, **kwargs):
    for attempt in range(1, retries + 1):
        try:
            return func(*args, **kwargs)
        except TooManyRequests:
            time.sleep(attempt * 60)
            print(f"Rate-limited. Retrying: Attempt {attempt}")
        except Exception as e:
            print(f"Unhandled Error: {e}")
            break
    return None

if __name__ == "__main__":
    spanish_subreddits = {}
    subreddits_checked = set()
    keywords = [
    # General Spanish terms
    "spanish", "español", "espanol", "castellano", "idioma", "lengua", "hispano", "latino", "latina", "españa",

    # Names of Spanish-speaking countries
    "mexico", "argentina", "colombia", "venezuela", "chile", "peru", "ecuador", "bolivia", "paraguay", "uruguay",
    "cuba", "guatemala", "honduras", "el salvador", "nicaragua", "costa rica", "panama", "puerto rico", "dominican republic",
    "republica dominicana", "españa", "spain", "andorra", "equatorial guinea", "guinea ecuatorial", "philippines",

    # Names of major Spanish-speaking cities
    "madrid", "barcelona", "buenos aires", "mexico city", "bogota", "lima", "santiago", "quito", "caracas", "asuncion",
    "montevideo", "san juan", "havana", "guadalajara", "medellin", "valencia", "sevilla", "malaga",

    # Common Spanish topics/words
    "música", "deportes", "fútbol", "cine", "películas", "libros", "literatura", "comida", "recetas", "viajes",
    "vacaciones", "idiomas", "educación", "arte", "historia", "cultura", "salud", "tecnología", "política", "noticias",
    "ciencia", "naturaleza", "medio ambiente", "juegos", "videojuegos", "animales", "mascotas", "familia", "amor",

    # Common Spanish verbs/nouns
    "hablar", "aprender", "vivir", "viajar", "trabajo", "dinero", "estudiar", "leer", "escribir", "escuchar",
    "cantar", "bailar", "cocinar", "comer", "beber", "caminar", "deporte", "fútbol", "amistad", "vida",

    # Spanish slang/colloquial terms
    "chevere", "guay", "tio", "wey", "chido", "pura vida", "vale", "genial", "chavo", "chava", "onda",

    # Names of holidays or celebrations
    "día de los muertos", "navidad", "semana santa", "carnaval", "fiesta", "feria", "quinceañera", "san fermín",
    "cinco de mayo", "independencia",

    ]


    for keyword in keywords:
        subreddits = []
        try:
            results = fetch_with_retries(reddit.subreddits.search, keyword, limit=NUM_POSTS)
            if not results:
                continue
            for subreddit in results:
                if subreddit.display_name not in subreddits_checked:
                    subreddits_checked.add(subreddit.display_name)
                    print(f"Checking subreddit: {subreddit.display_name}")
                    if is_spanish_subreddit(subreddit) and subreddit.subscribers:
                        if subreddit.subscribers >= MIN_MEMBERS:
                            subreddits.append({
                                "name": subreddit.display_name,
                                "subscribers": subreddit.subscribers,
                            })
                            print(f"Subreddit Passed: {subreddit.display_name}")
            spanish_subreddits[keyword] = subreddits
        except Exception as e:
            print(f"Error processing word: {keyword}: {e}")

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(spanish_subreddits, f, ensure_ascii=False, indent=4)

    print("Search completed!")

