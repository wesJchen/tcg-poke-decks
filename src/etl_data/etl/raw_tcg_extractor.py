import os
from typing import Any, Dict, List

import psycopg2
from dotenv import load_dotenv
from pokemon_tcg_service import PokemonTCGServer
from psycopg2.extras import Json, execute_values

# Set up database connection
load_dotenv(override=True)


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

# SQL statements for raw cards table
create_sql = """
    CREATE TABLE IF NOT EXISTS raw_cards (
    data JSONB
);
"""

insert_sql = """
    INSERT INTO raw_cards (data)
    VALUES %s;
"""


def create_raw_table():
    """Creates the raw_cards table for unprocessed card data"""
    try:
        # Establish connection to the database
        with psycopg2.connect(**DB_CONFIG) as conn:
            # Create a cursor object to execute SQL commands
            with conn.cursor() as cursor:
                cursor.execute(create_sql)
    except Exception as e:
        print(f"Error creating raw_cards table: {e}")


def fetch_cards_data():
    """Fetches cards data from the API"""
    server = PokemonTCGServer()
    response = server.get_cards(
        page_size=10, order_by="set.releaseDate", query="set.name:generations"
    )
    cards = response.get("data", [])
    breakpoint()
    return cards


def load_to_db(cards: List[Dict[str, Any]]):
    """Inserts cards into the raw_cards table"""
    if not cards:
        print("No cards to load")

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Prepare data as list of tuples
                values = [
                    (Json(card),) for card in cards
                ]  # card must be a dict, not a string
                # Bulk insert
                execute_values(cursor, insert_sql, values)
                print(f"Successfully inserted {len(cards)} cards into raw_cards table")
    except Exception as e:
        print(f"Error inserting cards into raw_cards table: {e}")


if __name__ == "__main__":

    create_raw_table()
    cards = fetch_cards_data()
    load_to_db(cards)
