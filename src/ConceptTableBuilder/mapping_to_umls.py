import src.UMLSConnector as connector
from .single_string_query import single_string_query
from .second_step import run_second_step
from .first_step import run_first_step
from .third_step import run_third_step
from config import *
import pandas as pd

def map_to_umls():
    print("> Reading data")
    df = pd.read_csv(BARE_TABLE_SAVE_PATH + "/" + BARE_TABLE_IN_FILE, nrows=None)
    print(f"     length: {len(df)}")

    df["name"] = df["name"].str.strip()

    print("> Establishing MySql connection")
    connection = connector.connect(
        host = MYSQL_HOST,
        database = MYSQL_DATABASE,
        user = MYSQL_USERNAME,
        password = MYSQL_PASSWORD)

    if not os.path.exists(BARE_TABLE_SAVE_PATH):
        os.makedirs(BARE_TABLE_SAVE_PATH)

    print("> STEP 1: Using MySQL keyword \"LIKE\" keyword")
    df = run_first_step(df, connection)
    df.to_csv(BARE_TABLE_SAVE_PATH + "/" + BARE_TABLE_OUT_FILE_STEP_1, index=False)

    print("> STEP 2: Using more complicated algorithm with MySQL keyword \"LIKE\" keyword")
    df = run_second_step(df, connection)
    df.to_csv(BARE_TABLE_SAVE_PATH + "/" + BARE_TABLE_OUT_FILE_STEP_2, index=False)

    print("> STEP 3: Using NGRAMS and Levenshtein distance between NGRAM and string")
    df = run_third_step(df, connection)
    df.to_csv(BARE_TABLE_SAVE_PATH + "/" + BARE_TABLE_OUT_FILE_STEP_3, index=False)

    print("> Adding the CUI column to full table")
    print("    > Reading")
    df_fulltext = pd.read_csv(DATA_PATH + "/" + FULL_TABLE_IN_FILE, nrows=None)
    print("    > Merging")
    df_final = pd.merge(df_fulltext, df[["name", "CUI"]], on="name")
    print("    > Saving")
    df_final.to_csv(DATA_PATH + "/" + FULL_TABLE_OUT_FILE, index=False)

    print("> Done.")