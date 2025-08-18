import os

import requests

"""
## API Documentation

# Get all cards
curl "https://api.pokemontcg.io/v2/cards"

# Get a single page of cards
curl "https://api.pokemontcg.io/v2/cards?page=1&pageSize=250"

# Filter cards via query parameters
curl "https://api.pokemontcg.io/v2/cards?q=set.name:generations subtypes:mega"

# Order by release date (descending)
curl "https://api.pokemontcg.io/v2/cards?q=subtypes:mega&orderBy=-set.releaseDate"
"""


class PokemonTCGServer:
    def __init__(self):
        self.base_url = "https://api.pokemontcg.io/v2"
        self.headers = {
            "Accept": "application/json",
            "X-Api-Key": os.getenv("POKEMON_TCG_API_KEY"),
        }

    def get_cards(self, page_size=None, order_by=None, query=None) -> dict:
        url = f"{self.base_url}/cards"
        params = {}
        if page_size:
            params.update({"pageSize": page_size})
        if order_by:
            params.update({"orderBy": order_by})
        if query:
            params.update({"q": query})

        response = requests.get(
            url=url,
            headers=self.headers,
            params=params,
        )
        return response.json()
