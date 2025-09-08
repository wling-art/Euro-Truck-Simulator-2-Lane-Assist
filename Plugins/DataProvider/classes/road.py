from Plugins.DataProvider.classes.base_item import BaseItem, ItemType


class RoadLook:
    __slots__ = [
        "token",
        "name",
        "lanes_left",
        "lanes_right",
        "offset",
        "shoulder_space_left",
        "shoulder_space_right",
    ]

    token: str
    name: str
    lanes_left: list[str]
    lanes_right: list[str]
    offset: float
    shoulder_space_left: float
    shoulder_space_right: float

    def __init__(
        self,
        token: str,
        name: str,
        lanes_left: list[str],
        lanes_right: list[str],
        offset: float | None,
        shoulder_space_left: float | None,
        shoulder_space_right: float | None,
    ):
        self.token = token
        self.name = name
        self.lanes_left = lanes_left
        self.lanes_right = lanes_right
        self.offset = offset
        self.shoulder_space_left = shoulder_space_left
        self.shoulder_space_right = shoulder_space_right

    def json(self) -> dict:
        return {
            "token": self.token,
            "name": self.name,
            "lanes_left": self.lanes_left,
            "lanes_right": self.lanes_right,
            "offset": self.offset,
            "shoulder_space_left": self.shoulder_space_left,
            "shoulder_space_right": self.shoulder_space_right,
        }

    def __str__(self) -> str:
        return f"RoadLook({self.token}, {self.name}, {self.lanes_left}, {self.lanes_right}, {self.offset}, {self.shoulder_space_left}, {self.shoulder_space_right})"

    def __repr__(self) -> str:
        return self.__str__()


class Railing:
    __slots__ = [
        "right_railing",
        "right_railing_offset",
        "left_railing",
        "left_railing_offset",
    ]

    right_railing: str
    right_railing_offset: int
    left_railing: str
    left_railing_offset: int

    def __init__(
        self,
        right_railing: str,
        right_railing_offset: int,
        left_railing: str,
        left_railing_offset: int,
    ):
        self.right_railing = right_railing
        self.right_railing_offset = right_railing_offset
        self.left_railing = left_railing
        self.left_railing_offset = left_railing_offset

    def json(self) -> dict:
        return {
            "right_railing": self.right_railing,
            "right_railing_offset": self.right_railing_offset,
            "left_railing": self.left_railing,
            "left_railing_offset": self.left_railing_offset,
        }


class Road(BaseItem):
    __slots__ = [
        "hidden",
        "road_look_token",
        "start_node_uid",
        "end_node_uid",
        "length",
        "maybe_divided",
        "type",
        "road_look",
        "railings",
    ]

    hidden: bool
    road_look_token: str
    start_node_uid: str
    end_node_uid: str
    length: float
    maybe_divided: bool
    type: ItemType
    road_look: RoadLook
    railings: list[Railing] | None

    def __init__(
        self,
        uid: int | str,
        x: float,
        y: float,
        hidden: bool | None,
        road_look_token: str,
        start_node_uid: str,
        end_node_uid: str,
        length: float,
        maybe_divided: bool | None,
        railings: list[Railing] | None = None,
    ):
        super().__init__(uid, ItemType.Road, x, y)

        self.type = ItemType.Road
        self.hidden = bool(hidden) if hidden is not None else False
        self.road_look_token = road_look_token
        self.start_node_uid = start_node_uid
        self.end_node_uid = end_node_uid
        self.length = length
        self.maybe_divided = maybe_divided
        self.railings = railings if railings is not None else []
