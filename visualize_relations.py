# Import own modules
from src.RelationsTableVisualizer import Visualizer
# Import libraries
import pandas as pd
from config import *

def visualize_relations():
    print("Starting visualization program")
    print("> Reading table")

    relations_df = pd.read_csv("./saves/tables/mayoclinic_table_12-51-39_2022-08-04.csv")
    visualizer = Visualizer(
        data=relations_df,
        source_name="mayoclinic")
    visualizer.visualize_entire_source(edge_len="5.00")

    relations_df = pd.read_csv("./saves/tables/medline_table_12-52-25_2022-08-04.csv")
    visualizer = Visualizer(
        data=relations_df,
        source_name="medline")
    visualizer.visualize_entire_source(edge_len="20.00")

if __name__ == "__main__":
    visualize_relations()