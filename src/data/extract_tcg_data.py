import os

import requests


class PokemonTCGExtractor:
    def __init__(self):
        self.base_url = "https://api.pokemontcg.io/v2"
        self.headers = {
            "Accept": "application/json",
            "X-Api-Key": os.getenv("POKEMON_TCG_API_KEY"),
        }

    def get_cards(self, set_code: str) -> list:
        url = f"{self.base_url}/cards"
        response = requests.get(url, headers=self.headers)
        return response.json()


if __name__ == "__main__":
    extractor = PokemonTCGExtractor()
    cards = extractor.get_cards("base1")
    print(cards)
