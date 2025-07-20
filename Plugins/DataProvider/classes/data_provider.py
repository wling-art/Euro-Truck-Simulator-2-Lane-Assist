from Plugins.DataProvider.classes.node import Node
from Plugins.DataProvider.classes.road import Road
from Plugins.DataProvider.classes.prefab import Prefab

from typing import Optional

class DataProvider():
    """
    The DataProvider is used to store all the data parsed from the files.
    Basically it just gives an easy way to lookup nodes and items based on their UIDs.
    """
    nodes: dict[str, Node] = {}
    roads: dict[str, Road] = {}
    prefabs: dict[str, Prefab] = {}
    
    def get_node(self, uid: str) -> Optional[Node]:
        """Get a node by its unique ID."""
        return self.nodes.get(uid)
    
    def get_item(self, uid: str) -> Optional[Road | Prefab]:
        """
        Get an item (node, road, or prefab) by its unique ID.
        Returns None if the item is not found.
        """
        return self.roads.get(uid) or self.prefabs.get(uid)