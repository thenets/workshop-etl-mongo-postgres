# %% Get params and import libs
from dotenv import load_dotenv

load_dotenv()

import os
import requests
import json

# %% Get Mongo client
from pymongo import MongoClient

if "MONGO_URL" in os.environ:
    mongo = MongoClient(os.environ["MONGO_URL"])
else:
    mongo = MongoClient()

# %% Populate Mongo database if not exist
def pokeapi_get_pokemon_by_id(pokemon_id: int):
    url = f"https://pokeapi-cache.herokuapp.com/api/v2/pokemon/{pokemon_id}"
    r = requests.get(url)
    return json.loads(r.content)


def mongo_insert_pokemon(pokemon: dict, log_stdout=True):
    m_pokedex = mongo.get_database("pokedex")
    m_pokedex_pokemon = m_pokedex.get_collection("pokemon")
    m_pokedex_pokemon.insert_one(pokemon)
    if log_stdout:
        print(f"[INSERTED] {pokemon['name']}")


def mongo_insert_pokemon_by_id(pokemon_id: int):
    pokemon = pokeapi_get_pokemon_by_id(pokemon_id)
    mongo_insert_pokemon(pokemon)


def mongo_get_pokemon_by_name(pokemon_name: str):
    m_pokedex = mongo.get_database("pokedex")
    m_pokedex_pokemon = m_pokedex.get_collection("pokemon")
    return m_pokedex_pokemon.find_one({"name": pokemon_name})


database_names = [x["name"] for x in mongo.list_databases()]

if "pokedex" not in database_names:
    populate_async = True  # Param
    pokedex_up_to = 40

    if populate_async:
        from multiprocessing import Pool, TimeoutError
        import time
        import os

        print(f"[PokeAPI] Retrieving data of {pokedex_up_to} Pokémon.")
        with Pool(processes=10) as pool:
            print("          downloading... (timeout of 120s)")
            pokemon_list = pool.map_async(
                pokeapi_get_pokemon_by_id, range(pokedex_up_to + 1)[1:]
            ).get(timeout=120)
            for pokemon in pokemon_list:
                mongo_insert_pokemon(pokemon, False)
            print("          download complete!")
    else:
        for i in range(pokedex_up_to + 1)[1:]:
            mongo_insert_pokemon(pokeapi_get_pokemon_by_id(i))


# %% Create PostgreSQL tables
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import inspect
from sqlalchemy import Table
from sqlalchemy import Column, Integer, String
from sqlalchemy.engine.url import URL

db_url = {
    "drivername": "postgres",
    "username": os.environ["POSTGRESQL_USER"],
    "password": os.environ["POSTGRESQL_PASS"],
    "host": os.environ["POSTGRESQL_HOST"],
    "port": os.environ["POSTGRESQL_PORT"],
    "database": os.environ["POSTGRESQL_DB"],
}
engine = create_engine(URL(**db_url))
m = MetaData()

db_table_name = "moves"

# %%
table = Table(
    db_table_name,
    m,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False, unique=True),
    Column("url", String, nullable=False),
)

table.create(engine)
inspector = inspect(engine)
print(db_table_name in inspector.get_table_names())

# %%
pokemon_list = [pokeapi_get_pokemon_by_id(25)]
moves_list = []

for pokemon in pokemon_list:
    for move in pokemon["moves"]:
        moves_list.append({"name": move["move"]["name"], "url": move["move"]["url"]})

# %%
import pandas as pd

df = pd.DataFrame().from_dict(moves_list)
df.head()

df.to_sql(
    name=db_table_name, schema="public", con=engine, if_exists="append", index=False
)


# %% Drop PostgreSQL database
table.drop(engine)
inspector = inspect(engine)
print(db_table_name in inspector.get_table_names())

# %%
