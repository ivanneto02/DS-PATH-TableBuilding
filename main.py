# Import our own modules
import src.RelRowStrategy as StrategyModule
import src.RelationsTableBuilder as TableModule

# Import libraries
import pandas as pd

from config import *

def main():
    print("> Starting")
    print("> Reading data")
    df = pd.read_csv(PATH_TO_DATA + "/" + DATA_FILE)
    slices = ["mayoclinic"]

    print("> Slicing based on sources")
    df = df[ (df["source_name"] in slices) & (df["concept_type"] == "drug") ]

    print(df["source_name"].value_counts())
    pass

if __name__ == "__main__":
    main()