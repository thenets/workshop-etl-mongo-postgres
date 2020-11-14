# %% Get params and import libs
from dotenv import load_dotenv
load_dotenv()

import os

# %% Import data from DocumentDB
from pymongo import MongoClient
if 'MONGO_URL' in os.environ:
    mongo_client = MongoClient(os.environ['MONGO_URL'])
else:
    mongo_client = MongoClient()

# %% Populate database if not exist
database_names = [x['name'] for x in mongo_client.list_databases()]

if 'pokedex' not in database_names:
    mongo_client.data
database_names

# %%
import pandas as pd

jobs_df = pd.read_csv('data/nyc-jobs.csv')

print("OI")


# %%
from sqlalchemy.types import Integer, Text, String, DateTime
