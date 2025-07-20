from Plugins.DataProvider.classes import Transform, Rotation

class Node:
    __slots__ = ['uid', 'transform', 'forward_item_uid', 'backward_item_uid']
    
    uid: str
    transform: Transform
    forward_item_uid: str
    backward_item_uid: str

    def __init__(self, uid: int | str, x: float, y: float, z: float, rotationQuat: list[float], 
                 forward_item_uid: int | str, backward_item_uid: int | str):
        self.uid = uid
        
        self.transform = Transform(x, y, z, Rotation(*rotationQuat))
        
        self.forward_item_uid = forward_item_uid
        self.backward_item_uid = backward_item_uid
        
    def json(self) -> dict:
        return {
            "uid": self.uid,
            "transform": self.transform.json(),
            "forward_item_uid": self.forward_item_uid,
            "backward_item_uid": self.backward_item_uid,
        }