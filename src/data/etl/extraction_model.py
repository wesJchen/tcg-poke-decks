# import pandas as pd
from api_helpers import PokemonTCGServer

server = PokemonTCGServer()
cards = server.get_cards("base1")
print(cards)
