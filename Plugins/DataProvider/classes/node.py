from Plugins.DataProvider.utils import math as umath
from Plugins.DataProvider.classes.navigation import NavigationEntry

class Node:
    __slots__ = ['uid', 'x', 'y', 'z', 'rotationQuat', '_euler', 'forward_item_uid', 'backward_item_uid', 'navigation']
    
    uid: str
    x: float
    y: float
    z: float
    rotationQuat: list[float]
    _euler: list[float]
    forward_item_uid: str
    backward_item_uid: str
    navigation: NavigationEntry

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
        
        self.navigation = None
        
    @property
    def euler(self) -> list[float]:
        if self._euler is None:
            self._euler = umath.quat_to_euler(self.rotationQuat)
        return self._euler

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