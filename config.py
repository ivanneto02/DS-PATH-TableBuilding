from dotenv import load_dotenv
import os

load_dotenv()

PATH_TO_DATA = os.environ["PATH_TO_DATA"]
DATA_FILE = os.environ["DATA_FILE"]
N_ROWS = int(os.environ["N_ROWS"]) if "none" not in os.environ["N_ROWS"].lower() else None # use "None" in .env to indicate all rows

MYSQL_USERNAME = os.environ["_MYSQL_USERNAME"]
MYSQL_PASSWORD = os.environ["_MYSQL_PASSWORD"]
MYSQL_PORT = os.environ["_MYSQL_PORT"]
MYSQL_HOST = os.environ["_MYSQL_HOST"]
MYSQL_DATABASE = os.environ["_MYSQL_DB"]