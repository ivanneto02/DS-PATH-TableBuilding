# Import own modules
from src.RelationsTableVisualizer import Visualizer
# Import libraries
import pandas as pd
from config import *

def visualize_relations():
    print("Starting visualization program")
    print("> Reading table")

    relations_df = pd.read_csv("./saves/tables/medline_table_06-43-18_2022-07-21.csv")
    visualizer = Visualizer(
        data=relations_df,
        source_name="medline")
    
    visualizer.visualize_entire_source()

if __name__ == "__main__":
    visualize_relations()