import requests
from bs4 import BeautifulSoup


def scrape_github_trending():
    url = "https://github.com/trending"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    repo_cards = soup.find_all("article", class_="Box-row")

    results = []

    for card in repo_cards:
        name_tag = card.find("a", attrs={"data-view-component": "true", "class": "Link"})
        if not name_tag:
            continue
        repo_full_name = name_tag["href"].strip("/")
        repo_name = repo_full_name.split("/")[-1]

        language_tag = card.find("span", attrs={"itemprop": "programmingLanguage"})
        language = language_tag.text.strip() if language_tag else None

        stars_today_tag = card.find("span", class_="d-inline-block float-sm-right")
        if stars_today_tag:
            stars_text = stars_today_tag.text.strip()
            stars_today = int(stars_text.split()[0].replace(",", ""))
        else:
            stars_today = 0

        results.append({
            "repo_name": repo_name,
            "language": language,
            "stars_today": stars_today,
        })

    return results