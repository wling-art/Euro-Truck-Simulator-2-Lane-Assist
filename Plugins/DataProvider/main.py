from ETS2LA.Utils.translator import _
from ETS2LA.Plugin import *
import rich

from Modules.TruckSimAPI.main import Module as TruckSimAPI

from Plugins.DataProvider.classes.data_provider import DataProvider
from Plugins.DataProvider.utils import memory
from Plugins.DataProvider.classes import *
from Plugins.DataProvider import reader

class Plugin(ETS2LAPlugin):
    description = PluginDescription(
        name=_("Data Provider"),
        description=_("Provides map data for other plugins."),
        version="1.0.0",
        fps_cap=1,
        tags=["Base"]
    )
    
    author = [
        Author(
            name="Tumppi066",
            url="https://github.com/Tumppi066",
            icon="https://avatars.githubusercontent.com/u/83072683?v=4"
        )
    ]
    
    provider = DataProvider()
    
    def init(self) -> None:
        self.api = TruckSimAPI(self)
        self.api.init()
        
    def load_data(self) -> None:
        # Nodes
        self.state.text = _("Loading nodes...")
        start = memory.read_memory_usage()
        nodes = reader.read_nodes()
        self.provider.nodes = {node.uid: node for node in nodes}

        print(f"Loaded {len(self.provider.nodes)} nodes from data provider.")
        end = memory.read_memory_usage()
        print(f"Memory usage: {end - start:.2f} MB")
        
        # Roads
        self.state.text = _("Loading roads...")
        start = memory.read_memory_usage()
        roads = reader.read_roads()
        road_looks = reader.read_road_looks()
        for road in roads:
            if road.road_look_token in road_looks:
                road.road_look = road_looks[road.road_look_token]
            else:
                road.road_look = RoadLook(road.road_look_token, "Unknown", [], [], None, None, None)

        self.provider.roads = {road.uid: road for road in roads}
        del roads
        del road_looks

        print(f"Loaded {len(self.provider.roads)} roads from data provider.")
        end = memory.read_memory_usage()
        print(f"Memory usage: {end - start:.2f} MB")
            
        # Prefabs
        self.state.text = _("Loading prefabs...")
        start = memory.read_memory_usage()
        prefabs = reader.read_prefabs()
        self.provider.prefabs = {prefab.uid: prefab for prefab in prefabs}
        del prefabs
        
        descriptions = reader.read_prefab_descriptions()
        descriptions = {description.token: description for description in descriptions}
        for prefab in self.provider.prefabs.values():
            if prefab.token in descriptions:
                prefab.description = descriptions[prefab.token]
            else:
                prefab.description = None
        
        del descriptions
        print(f"Loaded {len(self.prefabs)} prefabs from data provider.")
        end = memory.read_memory_usage()
        print(f"Memory usage: {end - start:.2f} MB")
        
        self.state.reset()
        
    def parse_lanes(self):
        for road in self.provider.roads.values():
            lane = Lane()
        
    def run(self) -> None:
        data = self.api.run()
        if not self.provider.prefabs or not self.provider.nodes or not self.provider.roads:
            self.load_data()