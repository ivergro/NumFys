import Disc

class CollisionObject:
    __slots__ = ("object_1", "object_2", "collision_counter")

    def __init__(self, ob_1 : Disc, ob_2):
        self.object_1 = ob_1
        self.object_2 = ob_2

        #Calculating collision counter to discard invalid collisions
        if isinstance(ob_2, str):
            self.collision_counter = ob_1.collision_count
        else:   
            self.collision_counter = ob_1.collision_count + ob_2.collision_count