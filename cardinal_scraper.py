import requests
from bs4 import BeautifulSoup
import json

def fetch_cardinal_electors():
    url = "https://www.catholic-hierarchy.org/bishop/scardc3.html"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")

    # 1) Find the table by its <h1>
    header = soup.find("h1", string="Cardinal Electors")
    if not header:
        raise RuntimeError("Couldn't find the 'Cardinal Electors' heading")
    table = header.find_next("table")
    if not table:
        raise RuntimeError("Couldn't find the electors table")

    cardinals = []
    for tr in table.find_all("tr")[1:]:
        cols = tr.find_all("td")
        if len(cols) < 5:
            continue

        # 2) Extract and clean the name (4th cell)
        name_cell = cols[3]
        # Use a space‐separator so tags don't jam together, then strip “Cardinal”
        name = name_cell.get_text(" ", strip=True).replace("Cardinal", "").strip()

        # 3) Extract office & country (5th cell)
        title_cell = cols[4]
        # Identify only the real country links (href starting with "/country/")
        country_links = [
            a for a in title_cell.find_all("a")
            if a.get("href", "").startswith("/country/")
        ]
        country = country_links[-1].get_text(strip=True) \
                  if country_links else ""

        # Build the full text of the cell (with spaces between tags)
        full_text = title_cell.get_text(" ", strip=True)
        if country:
            # Split off the country from the end, then trim trailing commas/spaces
            office = full_text.rsplit(country, 1)[0].rstrip(", ").strip()
        else:
            office = full_text

        cardinals.append({
            "name":    name,
            "title":   office,
            "country": country,
            "image":   ""
        })

    return cardinals

if __name__ == "__main__":
    electors = fetch_cardinal_electors()
    print(json.dumps(electors, ensure_ascii=False, indent=2))