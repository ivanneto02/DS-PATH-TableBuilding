# Import own modules
from src.RelationsTableVisualizer import Visualizer
# Import libraries
import pandas as pd
from config import *

def visualize_relations():
    print("Starting visualization program")
    print("> Reading table")

    relations_df = pd.read_csv("./saves/tables/mayoclinic_table_14-22-23_2022-08-12.csv")[:3000]
    visualizer = Visualizer(
        data=relations_df,
        source_name="mayoclinic")
    visualizer.visualize_entire_source(edge_len="5.00")

    relations_df = pd.read_csv("./saves/tables/medline_table_14-23-14_2022-08-12.csv")[:3000]
    visualizer = Visualizer(
        data=relations_df,
        source_name="medline")
    visualizer.visualize_entire_source(edge_len="20.00")

    relations_df = pd.read_csv("./saves/tables/drugs.com_table_19-26-49_2022-08-12.csv")[:3000]
    visualizer = Visualizer(
        data=relations_df,
        source_name="drugs.com")
    visualizer.visualize_entire_source(edge_len="6.00")

if __name__ == "__main__":
    visualize_relations()