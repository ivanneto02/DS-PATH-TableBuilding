import graphviz
import os
from datetime import datetime
import numpy as np

class Visualizer():
    def __init__(self, data, source_name):
        self.data = data
        self.source_name = source_name

    def visualize_single_concept(self, concept_name):
        # Determine slice to visualize
        df = self.data
        df = df[df["from_string"] == concept_name]
        known_concepts = []
        # Create graph
        gra = graphviz.Digraph(
            engine="neato",
            node_attr={"color" : "aquamarine", "style" : "filled"},
            edge_attr={"len" : "50.0"},
            format="svg")
        # Create from_string concept onde
        gra.node(concept_name, concept_name)
        for index, row in df.iterrows():
            if row["to_string"] in known_concepts:
                continue
            gra.node(row["to_string"], row["to_string"])
            gra.edge(concept_name, row["to_string"], label=row["rel_type"])
            known_concepts.append(row["to_string"])
        gra = gra.unflatten(stagger=50)
        if not os.path.exists("./saves/graphs/"):
            os.makedirs("./saves/graphs/")
        gra.render("./saves/graphs/" + f'{self.source_name}_{concept_name}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')

    def visualize_all_discrete_concepts(self):
        print(f"> Visualizing every concept in '{self.source_name}' source. This may take a moment.")
        for concept in np.unique(self.data["from_string"]):
            self.visualize_single_concept(concept)

    def visualize_entire_source(self):
        print("> Visualizing entire source in big graph. This may take a while.")
        df = self.data

        source_name = self.data["source_name"].iloc[0]

        gra = graphviz.Digraph(
            engine="neato",
            graph_attr={
                "label" : f"Source: {source_name}",
                "labelloc" : "t"},
            node_attr={"color" : "aquamarine", "style" : "filled"},
            edge_attr={"len" : "20.0"},
            format="svg")

        known_concepts = []
        edges = []
        for index, row in self.data.iterrows():
            if row["from_string"] not in known_concepts:
                gra.node(str(row["from_string"]), str(row["from_string"]))
                known_concepts.append(row["from_string"])
            if row["to_string"] not in known_concepts:
                gra.node(str(row["to_string"]), str(row["to_string"]))
                known_concepts.append(row["to_string"])
            if (row["from_string"], row["to_string"]) not in edges:
                gra.edge(str(row["from_string"]), str(row["to_string"]), label=row["rel_type"])
                edges.append((row["from_string"], row["to_string"]))
        gra = gra.unflatten(stagger=10)
        if not os.path.exists("./saves/graphs/"):
            os.makedirs("./saves/graphs/")
        gra.render("./saves/graphs/" + f'{self.source_name}_table_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')