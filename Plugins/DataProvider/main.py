from ETS2LA.Plugin import *
from ETS2LA.Utils.translator import _

from Modules.TruckSimAPI.main import Module as TruckSimAPI

from Plugins.DataProvider.classes import Node
from Plugins.DataProvider import reader
from Plugins.DataProvider.utils import memory

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
    
    nodes: list[Node] = []
    
    def init(self) -> None:
        self.api = TruckSimAPI(self)
        self.api.init()
        
    def run(self) -> None:
        data = self.api.run()
        
        if not self.nodes:
            start = memory.read_memory_usage()
            self.nodes = reader.read_nodes()
            print(f"Loaded {len(self.nodes)} nodes from data provider.")
            end = memory.read_memory_usage()
            print(f"Memory usage: {end - start:.2f} MB")