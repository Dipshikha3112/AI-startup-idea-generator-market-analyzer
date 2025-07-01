import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def search_competitors(query, max_results=5):
    search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", attrs={"class": "result__a"}, limit=max_results)

        competitors = []
        for result in results:
            title = result.get_text()
            if re.search(r"(edtech|startup|platform|learning|education)", title, re.I):
                competitors.append(title)

        return competitors, len(competitors)
    except Exception as e:
        print(f"Search error: {e}")
        return [], 0
