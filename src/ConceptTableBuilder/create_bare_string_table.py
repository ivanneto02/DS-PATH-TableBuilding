from multiprocessing.sharedctypes import Value
from xml.etree.ElementTree import QName
from config import *
import src.UMLSConnector as connector
from datetime import datetime

def create_bare_string_table():
    return
    print("> Starting the visualization process")
    print("> Creating connection")
    # connect to database, return connection
    connection = connector.connect(
        host = MYSQL_HOST,
        database = MYSQL_DATABASE,
        user = MYSQL_USERNAME,
        password = MYSQL_PASSWORD)

    print("> Making relations dictionary")
    relations_dictionary = {}
    for result in relations_results:
        if result[0][0] not in relations_dictionary.keys():
            relations_dictionary[result[0][0]] = []
            for row in result:
                relations_dictionary[row[0]].append(row[3])

    print("> Done")
    print("> Making graph")
    nodes = []
    edges = []
    grap = graphviz.Digraph(
        engine="neato",
        edge_attr={"len" : "7.0"},
        graph_attr={"overlap" : "false"},
        format="svg",
        node_attr={"colormap" : "greens9", "style" : "filled"}
    )

    # for every single row in this query
    for i in range(len(relations_results)):
        for j in range(len(relations_results[i])):
            key = relations_results[i][j][0]
            value = relations_results[i][j][3]
            edge_label = relations_results[i][j][1]+"\n"+relations_results[i][j][2]
            if relations_results[i][j][0] not in nodes:
                in_node_label = relations_results[i][j][0]+"\n"+strings_dic[relations_results[i][j][0]]
                grap.node(key, label=in_node_label)
                nodes.append(key)
            if relations_results[i][j][3] not in nodes:
                out_node_label = relations_results[i][j][3]+"\n"+strings_dic[relations_results[i][j][3]]
                grap.node(value, label=out_node_label)
                nodes.append(value)
            if (key, value) not in edges:
                grap.edge(key, value, label=edge_label)
                edges.append((key, value))

    print("> Done")
    print("> Rendering and saving")
    grap = grap.unflatten(stagger=1000, chain=50)
    grap.render(image_save_path + f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_FULL_RXNORM', view=True)
    print("> Done")
    print("> Disconnecting")
    # will disconnect the connection
    connector.disconnect(connection)