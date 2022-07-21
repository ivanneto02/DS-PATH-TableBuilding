from dotenv import load_dotenv
import os

load_dotenv()

PATH_TO_DATA = os.environ["PATH_TO_DATA"]
DATA_FILE = os.environ["DATA_FILE"]
N_ROWS = int(os.environ["N_ROWS"]) if "none" not in os.environ["N_ROWS"].lower() else None # use "None" in .env to indicate all rows