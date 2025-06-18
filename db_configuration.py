import os
from dotenv import load_dotenv
from pprint import pprint


# pprint(dict(os.environ)) # list all env variables

# Load environment variables from .env file
env_path = os.getenv("dotenv_file")
load_dotenv(env_path)

db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_name = os.getenv("DB_NAME")

