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

def read_roads() -> list[Road]:
    path = find_category_file("roads")
    if path is None: return []
    roads: list[Road] = []
    file = orjson.loads(open(path, "rb").read())
    for road in file:
        roads.append(Road(
            road["uid"],
            road["x"],
            road["y"],
            bool(road.get("hidden", False)),
            road["roadLookToken"],
            road["startNodeUid"],
            road["endNodeUid"],
            road["length"],
            road.get("maybeDivided", False),
            [
                Railing(
                    railing["rightRailing"],
                    railing["rightRailingOffset"],
                    railing["leftRailing"],
                    railing["leftRailingOffset"]
                ) for railing in road.get("railings", [])
            ]
        ))

    return roads

def read_road_looks() -> dict[str, RoadLook]:
    path = find_category_file("roadLooks")
    if path is None: return {}
    road_looks: dict[str, RoadLook] = {}
    file = orjson.loads(open(path, "rb").read())
    for road_look in file:
        road_looks[road_look["token"]] = RoadLook(
            road_look["token"],
            road_look["name"],
            road_look.get("lanesLeft", []),
            road_look.get("lanesRight", []),
            road_look.get("offset", 0),
            road_look.get("shoulderSpaceRight", 0),
            road_look.get("shoulderSpaceLeft", 0),
        )

    return road_looks