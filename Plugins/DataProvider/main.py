from ETS2LA.Utils.translator import _
from ETS2LA.Plugin import *
import rich

from Modules.TruckSimAPI.main import Module as TruckSimAPI

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
    
    nodes: dict[str, Node] = {}
    
    def init(self) -> None:
        self.api = TruckSimAPI(self)
        self.api.init()
        
    def run(self) -> None:
        data = self.api.run()
        
        if not self.nodes:
            start = memory.read_memory_usage()
            nodes = reader.read_nodes()
            
            nav = reader.read_navigation()
            self.nodes = {node.uid: node for node in nodes}
            for entry in nav:
                self.nodes[entry.uid].navigation = entry
            del nav
            
            print(f"Loaded {len(self.nodes)} nodes from data provider.")
            end = memory.read_memory_usage()
            print(f"Memory usage: {end - start:.2f} MB")
            rich.print_json(data=self.nodes[next(iter(self.nodes))].json())