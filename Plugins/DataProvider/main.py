from ETS2LA.Utils.translator import _
from ETS2LA.Plugin import ETS2LAPlugin, PluginDescription, Author

from Modules.TruckSimAPI.main import Module as TruckSimAPI

from Plugins.DataProvider.classes.data_provider import DataProvider
from Plugins.DataProvider.utils import memory
from Plugins.DataProvider.classes import Road, RoadLook, Lane, Prefab
from Plugins.DataProvider import reader

from typing import Literal
from rich import print
import time


class Plugin(ETS2LAPlugin):
    description = PluginDescription(
        name=_("Data Provider"),
        description=_("Provides map data for other plugins."),
        version="1.0.0",
        fps_cap=1,
        tags=["Base"],
    )

    author = [
        Author(
            name="Tumppi066",
            url="https://github.com/Tumppi066",
            icon="https://avatars.githubusercontent.com/u/83072683?v=4",
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
                road.road_look = RoadLook(
                    road.road_look_token, "Unknown", [], [], None, None, None
                )

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
        print(f"Loaded {len(self.provider.prefabs)} prefabs from data provider.")
        end = memory.read_memory_usage()
        print(f"Memory usage: {end - start:.2f} MB")

    def create_lane_for_road(
        self, road: Road, side: Literal["left", "right"], index: int
    ) -> Lane:
        lane = Lane()
        lane.item = road
        lane.item_type = "road"
        lane.item_uid = road.uid

        lane.index = index
        lane.side = side
        lane.type = "normal"  # TODO: Parse lane type (use the RoadLook data)
        # TODO: Parse markings, railings, rules, probably as a processing step after?

        return lane

    def process_road_lanes(self, lanes: list[Lane]) -> None:
        last_lane: Lane | None = None
        for i, lane in enumerate(lanes):
            if not last_lane:
                lane.markings.left.type = "solid"
                last_lane = lane
                continue

            if last_lane.side == lane.side:
                last_lane.right = lane
                lane.left = last_lane
                last_lane.markings.right.type = "dashed"
                lane.markings.left.type = "dashed"

            if last_lane.side != lane.side:
                # TODO: Check if the lanes are connected, if so, use dashed lines
                last_lane.markings.right.type = "solid"
                lane.markings.left.type = "solid"

            if i == len(lanes) - 1:
                if last_lane:
                    lane.left = last_lane
                lane.markings.right.type = "solid"

            last_lane = lane

    def parse_road(self, road: Road) -> list[Lane]:
        lanes: list[Lane] = []
        index = 0
        for _lane in road.road_look.lanes_left:
            lane_instance = self.create_lane_for_road(road, "left", index)
            index += 1
            if lane_instance:
                lanes.append(lane_instance)

        for _lane in road.road_look.lanes_right:
            lane_instance = self.create_lane_for_road(road, "right", index)
            index += 1
            if lane_instance:
                lanes.append(lane_instance)

        self.process_road_lanes(lanes)
        return lanes

    def parse_prefab(self, prefab: Prefab) -> list[Lane]:
        lanes: list[Lane] = []
        index = 0
        for curve in prefab.description.nav_curves:
            lane = Lane()
            lane.item = prefab
            lane.item_type = "prefab"
            lane.item_uid = prefab.uid
            lane.index = index
            lane.side = "right"  # Prefabs only have right side lanes
            lane.type = "normal"  # TODO: Parse lane type (use surrounding roads)
            lane.semaphore_id = curve.semaphore_id

            lanes.append(lane)
            index += 1

        # Associate forward and backward
        for lane, curve in zip(lanes, prefab.description.nav_curves, strict=True):
            if curve.next_lines:
                lane.forward = [lanes[i] for i in curve.next_lines if i < len(lanes)]
            if curve.prev_lines:
                lane.backward = [lanes[i] for i in curve.prev_lines if i < len(lanes)]

        return lanes

    def find_routes_from_lane(self, lane: Lane, path=None):
        if path is None:
            path = []
        path = path + [lane]
        if not lane.forward:
            return [path]
        routes = []
        for next_lane in lane.forward:
            new_paths = self.find_routes_from_lane(next_lane, path)
            for new_path in new_paths:
                routes.append(new_path)
        return routes

    def parse_lanes(self):
        self.state.text = _("Parsing road lanes...")
        for road in self.provider.roads.values():
            lanes = self.parse_road(road)
            self.provider.lanes[road.uid] = lanes

        self.state.text = _("Parsing prefab lanes...")
        for prefab in self.provider.prefabs.values():
            lanes = self.parse_prefab(prefab)
            self.provider.lanes[prefab.uid] = lanes

    def run(self) -> None:
        # data = self.api.run()
        start = memory.read_memory_usage()
        if (
            not self.provider.prefabs
            or not self.provider.nodes
            or not self.provider.roads
        ):
            self.load_data()

        self.parse_lanes()
        print(
            f"Total lanes parsed: {sum(len(lanes) for lanes in self.provider.lanes.values())}"
        )
        used = memory.read_memory_usage() - start
        print(f"Total memory use {used:.2f} MB")

        self.state.reset()
        time.sleep(60)
