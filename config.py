from dotenv import load_dotenv
import os

load_dotenv()

PATH_TO_DATA = os.environ["PATH_TO_DATA"]
DATA_FILE = os.environ["DATA_FILE"]
N_ROWS = int(os.environ["N_ROWS"]) if os.environ["N_ROWS"] != "None" else None