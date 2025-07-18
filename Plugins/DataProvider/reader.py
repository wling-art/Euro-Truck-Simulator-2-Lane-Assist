from Plugins.DataProvider.classes import *
import orjson
import json
import os

path = "Plugins/DataProvider/data"

def find_category_file(category: str) -> str:
    for file in os.listdir(path):
        if category in file and file.endswith(".json"):
            return os.path.join(path, file)
    return None

def read_nodes() -> list[Node]:
    path = find_category_file("nodes")
    if path is None: return []
    
    nodes: list[Node] = []
    #file = json.load(open(path, "r"))
    file = orjson.loads(open(path, "rb").read())
    for node in file:
        nodes.append(Node(
            node["uid"],
            node["x"],
            node["y"],
            node["z"],
            node["rotationQuat"],
            node["forwardItemUid"],
            node["backwardItemUid"],
        ))

    del file
    return nodes

def read_navigation() -> list[NavigationEntry]:
    path = find_category_file("graph")
    if path is None: return []
    
    entries: list[NavigationEntry] = []
    #file = json.load(open(path, "r"))
    file = orjson.loads(open(path, "rb").read())
    for entry in file:
        uid = entry[0]
        forward_nodes = [
            NavigationNode(
                node["nodeId"],
                node["distance"],
                node["direction"],
                node.get("isOneLaneRoad", False)
            ) 
            for node in entry[1]["forward"]
        ]
        backward_nodes = [
            NavigationNode(
                node["nodeId"],
                node["distance"],
                node["direction"],
                node.get("isOneLaneRoad", False)
            )
            for node in entry[1]["backward"]
        ]
        entries.append(NavigationEntry(uid, forward_nodes, backward_nodes))

    del file
    return entries