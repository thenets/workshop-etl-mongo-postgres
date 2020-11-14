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

def mongo_get_pokemon_by_name(pokemon_name: str):
    m_pokedex = mongo.get_database('pokedex')
    m_pokedex_pokemon = m_pokedex.get_collection('pokemon')
    return m_pokedex_pokemon.find_one({"name": pokemon_name})

database_names = [x['name'] for x in mongo.list_databases()]

if 'pokedex' not in database_names:
    for i in range(10):
        mongo_insert_pokemon(
            pokeapi_get_pokemon_by_id(i+1)
        )

# %%

# %%
import pandas as pd

jobs_df = pd.read_csv('data/nyc-jobs.csv')

print("OI")


# %%
from sqlalchemy.types import Integer, Text, String, DateTime
