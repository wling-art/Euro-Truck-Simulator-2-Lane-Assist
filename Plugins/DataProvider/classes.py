from Plugins.DataProvider.utils import math as math_helpers

def parse_string_to_int(string: str) -> int | None:
    if string is None: return None
    if isinstance(string, int): return string
    return int(string, 16)

class Node:
    __slots__ = ['uid', 'x', 'y', 'z', 'rotationQuat', '_euler', 'forward_item_uid', 'backward_item_uid', '_navigation']
    
    uid: str
    x: float
    y: float
    z: float
    rotationQuat: list[float]
    _euler: list[float]
    forward_item_uid: str
    backward_item_uid: str
    # _navigation: NavigationEntry

    def parse_strings(self):
        self.uid = parse_string_to_int(self.uid)
        self.forward_item_uid = parse_string_to_int(self.forward_item_uid)
        self.backward_item_uid = parse_string_to_int(self.backward_item_uid)

    def __init__(self, uid: int | str, x: float, y: float, z: float, rotationQuat: list[float], 
                 forward_item_uid: int | str, backward_item_uid: int | str):
        self.uid = uid
        
        self.x = x
        self.y = y
        self.z = z
        
        self.rotationQuat = rotationQuat
        self._euler = None
        
        self.forward_item_uid = forward_item_uid
        self.backward_item_uid = backward_item_uid
        
        self._navigation = None
        
        self.parse_strings()
        
    @property
    def euler(self) -> list[float]:
        if self._euler is None:
            self._euler = math_helpers.QuatToEuler(self.rotationQuat)
        return self._euler
        
    # @property
    # def navigation(self) -> NavigationEntry:
    #     if self._navigation is None:
    #         self._navigation = data.map.get_navigation_entry(self.uid)
    #     return self._navigation

    def json(self) -> dict:
        return {
            "uid": self.uid,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "rotationQuat": self.rotationQuat,
            "forward_item_uid": self.forward_item_uid,
            "backward_item_uid": self.backward_item_uid,
        }