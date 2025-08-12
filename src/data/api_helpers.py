import os

import pandas as pd
import requests


class PokemonTCGServer:
    def __init__(self):
        self.base_url = "https://api.pokemontcg.io/v2"
        self.headers = {
            "Accept": "application/json",
            "X-Api-Key": os.getenv("POKEMON_TCG_API_KEY"),
        }

    def get_cards(self, page_size=None, order_by=None) -> dict:
        url = f"{self.base_url}/cards"
        params = {}
        if page_size:
            params.update({"pageSize": page_size})
        if order_by:
            params.update({"orderBy": order_by})

        response = requests.get(
            url=url,
            headers=self.headers,
            params=params,
        )
        return response.json()

    def get_cards_dataframe(self, page_size=None, order_by=None) -> pd.DataFrame:
        """Get cards and return as a pandas DataFrame"""
        response = self.get_cards(page_size, order_by)

        if "data" not in response:
            print(f"Error: {response}")
            return pd.DataFrame()

        # Extract the cards data
        cards = response["data"]

        # Convert to DataFrame
        df = pd.DataFrame(cards)

        # Flatten nested attributes (like attacks, abilities, etc.)
        # You can customize this based on what fields you want
        flattened_df = self._flatten_card_data(df)

        return flattened_df

    def _flatten_card_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Flatten nested card data into columns"""
        # Create a copy to avoid modifying original
        result_df = df.copy()

        # Flatten common nested fields
        if "attacks" in result_df.columns:
            # Extract attack names and damage
            result_df["attack_names"] = result_df["attacks"].apply(
                lambda x: [attack.get("name", "") for attack in x] if x else []
            )
            result_df["attack_damage"] = result_df["attacks"].apply(
                lambda x: [attack.get("damage", "") for attack in x] if x else []
            )

        if "abilities" in result_df.columns:
            result_df["ability_names"] = result_df["abilities"].apply(
                lambda x: [ability.get("name", "") for ability in x] if x else []
            )

        if "types" in result_df.columns:
            result_df["types"] = result_df["types"].apply(
                lambda x: ", ".join(x) if x else ""
            )

        if "subtypes" in result_df.columns:
            result_df["subtypes"] = result_df["subtypes"].apply(
                lambda x: ", ".join(x) if x else ""
            )

        # Drop the original nested columns
        columns_to_drop = ["attacks", "abilities"]
        result_df = result_df.drop(
            columns=[col for col in columns_to_drop if col in result_df.columns]
        )

        return result_df


if __name__ == "__main__":
    server = PokemonTCGServer()

    # Get cards as DataFrame
    df = server.get_cards_dataframe(page_size=50)  # Start with 50 cards

    if not df.empty:
        print(f"Retrieved {len(df)} cards")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst few cards:")
        print(df[["name", "types", "hp", "rarity"]].head())

        # Save to CSV
        df.to_csv("pokemon_cards.csv", index=False)
        print(f"\nSaved {len(df)} cards to pokemon_cards.csv")

        # Show some statistics
        if "types" in df.columns:
            print(f"\nCard types: {df['types'].value_counts().to_dict()}")
    else:
        print("No cards retrieved")


"""
# Get all cards
curl "https://api.pokemontcg.io/v2/cards"

# Get a single page of cards
curl "https://api.pokemontcg.io/v2/cards?page=1&pageSize=250"

# Filter cards via query parameters
curl "https://api.pokemontcg.io/v2/cards?q=set.name:generations subtypes:mega"

# Order by release date (descending)
curl "https://api.pokemontcg.io/v2/cards?q=subtypes:mega&orderBy=-set.releaseDate"
"""
