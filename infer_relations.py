# Import our own modules
from src.RelationsTableBuilder import *
from src.RelRowStrategy import *
# Import libraries
import pandas as pd
from config import *
import datetime

def infer_relations():
    print("Starting relations inference program")
    print("> Starting")
    print("> Reading data")
    df = pd.read_csv(PATH_TO_DATA + "/" + DATA_FILE, nrows=N_ROWS)
    sources = ["mayoclinic", "medline"]

    print("Preprocessing")
    print("> Separating columns")
    columns = ["name", "raw_html", "source_name", "source_url", "concept_type", "date_time_scraped"]
    df = df[columns]

    print("> Slicing based on sources")
    df = df[df["concept_type"] == "drug"]
    df["source_name"] = df["source_name"].str.lower()
    slices = []
    
    print(df.head(10))

    for source in sources:
        curr = df[df["source_name"] == source]
        slices.append(curr)

    # This will call my creation packages
    for slice, source in zip(slices, sources):
        builder = None
        if source == "mayoclinic":
            builder = RelationsTableBuilder(slice, MayoclinicRelRowStrategy())
        elif source == "webmd":
            builder = RelationsTableBuilder(slice, WebMDRelRowStrategy())
        elif source == "medline":
            builder = RelationsTableBuilder(slice, MedlineplusStrategy())

        # Temporary until we find a fix
        # Currently some sources are NOT aligned with their source_name
        # Thus this fix is necessary
        builder.fix_sources() # TODO fix this up in scraping section

        # Build the table for each data slice
        builder.build_table()

        # Create directory if does not exist
        if not os.path.exists("./saves/tables/"):
            os.makedirs("./saves/tables/")
        # Dump the table into a csv file
        builder.dump_table(path="./saves/tables/", name=f"{source}_table_{datetime.datetime.now().strftime('%H-%M-%S_%Y-%m-%d')}")

if __name__ == "__main__":
    infer_relations()