import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


def scrape_letterboxd_list(list_url):
    movies = []
    page = 1

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    while True:
        url = f"{list_url}/page/{page}/"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        posters = soup.find_all("li", class_="posteritem")

        if not posters:
            break

        for poster in posters:
            film_div = poster.find("div", class_="react-component")
            title_year = film_div.get("data-item-name")

            match = re.match(r"^(.*)\s+\((\d{4})\)$", title_year)

            title = match.group(1)
            year = match.group(2)

            movies.append({
                "Film Title": title,
                "Release Year": int(year)
            })

        page += 1

    return pd.DataFrame(movies)


list_url = "https://letterboxd.com/fcbarcelona/list/movies-everyone-should-watch-at-least-once/"
df = scrape_letterboxd_list(list_url)

print(df)
df.to_excel("letterboxd_list.xlsx", index=False)
