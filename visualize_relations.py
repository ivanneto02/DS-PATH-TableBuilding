# Import own modules
from src.RelationsTableVisualizer import Visualizer
# Import libraries
import pandas as pd
from config import *

def visualize_relations():
    print("Starting visualization program")
    print("> Reading table")

    relations_df = pd.read_csv("./saves/tables/mayoclinic_table_03-01-17_2022-07-21.csv")
    visualizer = Visualizer(
        data=relations_df,
        source_name="mayoclinic")
    
    visualizer.visualize_single_concept("Analgesic Combination, Acetaminophen Salicylate (Oral Route)")
    visualizer.visualize_single_concept("Cough And Cold Combinations (Oral Route)")

if __name__ == "__main__":
    visualize_relations()