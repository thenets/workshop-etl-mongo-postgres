# %% Get params and import libs
from dotenv import load_dotenv
load_dotenv()

import os
import requests
import json

# %% Import data from DocumentDB
from pymongo import MongoClient
if 'MONGO_URL' in os.environ:
    mongo = MongoClient(os.environ['MONGO_URL'])
else:
    mongo = MongoClient()

# %% Populate database if not exist
def pokeapi_get_pokemon_by_id(pokemon_id: int):
    url = f"https://pokeapi-cache.herokuapp.com/api/v2/pokemon/{pokemon_id}"
    r = requests.get(url)
    return json.loads(r.content)

def mongo_insert_pokemon(pokemon: dict):
    m_pokedex = mongo.get_database('pokedex')
    m_pokedex_pokemon = m_pokedex.get_collection('pokemon')
    m_pokedex_pokemon.insert_one(pokemon)
    print(f"[INSERTED] {pokemon['name']}")

def mongo_insert_pokemon_by_id(pokemon_id: int):
    pokemon = pokeapi_get_pokemon_by_id(pokemon_id)
    mongo_insert_pokemon(pokemon)

def mongo_get_pokemon_by_name(pokemon_name: str):
    m_pokedex = mongo.get_database('pokedex')
    m_pokedex_pokemon = m_pokedex.get_collection('pokemon')
    return m_pokedex_pokemon.find_one({"name": pokemon_name})

database_names = [x['name'] for x in mongo.list_databases()]


# %%
if 'pokedex' not in database_names:
    populate_async = True
    pokedex_up_to = 220

    if populate_async:
        from multiprocessing import Pool, TimeoutError
        import time
        import os
        with Pool(processes=10) as pool:
            pool.map_async(
                mongo_insert_pokemon_by_id, range(pokedex_up_to+1)[1:]
            ).get(timeout=60)
    else:
        for i in range(pokedex_up_to+1)[1:]:
            mongo_insert_pokemon(
                pokeapi_get_pokemon_by_id(i)
            )

# %%
out

# %%
import pandas as pd

jobs_df = pd.read_csv('data/nyc-jobs.csv')

print("OI")


# %%
from sqlalchemy.types import Integer, Text, String, DateTime
