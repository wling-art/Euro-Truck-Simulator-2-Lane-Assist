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

def read_prefabs() -> list[Prefab]:
    path = find_category_file("prefabs")
    if path is None: return []
    prefabs: list[Prefab] = []
    file = orjson.loads(open(path, "rb").read())
    for prefab in file:
        prefabs.append(Prefab(
            prefab["uid"],
            prefab["x"],
            prefab["y"],
            prefab.get("z", 0.0),
            prefab.get("hidden", False),
            prefab["token"],
            [uid for uid in prefab["nodeUids"]],
            prefab["originNodeIndex"],
        ))

    return prefabs

import concurrent.futures
def read_prefab_descriptions() -> list[PrefabDescription]:
    path = find_category_file("prefabDescriptions")
    if path is None:
        return []

    prefab_data_list = orjson.loads(open(path, "rb").read())
    def process_prefab_description(prefab_description):
        # TODO: Read signs!
        return PrefabDescription(
            prefab_description["token"],
            # nodes
            [
                PrefabNode(
                    node["x"],
                    node["y"],
                    node["z"],
                    node["rotation"],
                    node.get("inputLanes", []),
                    node.get("outputLanes", []),
                )
                for node in prefab_description["nodes"]
            ],
            # map points
            [
                RoadMapPoint(
                    point["x"],
                    point["y"],
                    point["z"],
                    point["neighbors"],
                    point["lanesLeft"],
                    point["lanesRight"],
                    point["offset"],
                )
                if point["type"] == "road"
                else PolygonMapPoint(
                    point["x"],
                    point["y"],
                    point["z"],
                    point["neighbors"],
                    point["color"],
                    point["roadOver"],
                )
                if point["type"] == "polygon"
                else None
                for point in prefab_description["mapPoints"]
            ],
            # spawn points
            [
                PrefabSpawnPoints(
                    spawn_point["x"],
                    spawn_point["y"],
                    spawn_point.get("z", 0.0),
                    spawn_point["type"],
                )
                for spawn_point in prefab_description["spawnPoints"]
            ],
            # trigger points
            [
                PrefabTriggerPoint(
                    trigger_point["x"],
                    trigger_point["y"],
                    trigger_point.get("z", 0),
                    trigger_point["action"],
                )
                for trigger_point in prefab_description["triggerPoints"]
            ],
            # nav curves
            [
                PrefabNavCurve(
                    curve["navNodeIndex"],
                    Transform(
                        curve["start"]["x"],
                        curve["start"]["y"],
                        curve["start"]["z"],
                        curve["start"]["rotation"],
                    ),
                    Transform(
                        curve["end"]["x"],
                        curve["end"]["y"],
                        curve["end"]["z"],
                        curve["end"]["rotation"],
                    ),
                    curve["nextLines"],
                    curve["prevLines"],
                    curve.get("semaphoreId", -1)
                )
                for curve in prefab_description["navCurves"]
            ],
            # semaphores
            [
                Semaphore(
                    semaphore["x"],
                    semaphore["y"],
                    semaphore["z"],
                    semaphore["rotation"],
                    semaphore["type"],
                    semaphore["id"],
                )
                for semaphore in prefab_description.get("semaphores", [])
            ]
        )

    with concurrent.futures.ThreadPoolExecutor() as executor:
        prefab_descriptions = list(
            executor.map(process_prefab_description, prefab_data_list)
        )

    return prefab_descriptions