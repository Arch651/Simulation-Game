# store a tracker for enviornment elements

from src.utils.enums import (
    ElementType,
    EnviornmentTypes
)
from src.utils.mapper import mapper
from src.data_stores.tracker import Tracker
from src.enviornment.base import BaseEnviornment

class EnviornmentTracker:
    _instance = None
    _initialized  = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        window,
        board_size: int
    ):
        if self._initialized :
            return 
        
        self.window = window
        self.board_size: int = board_size
        self.tracker: dict[EnviornmentTypes,Tracker] = {
            key: Tracker(
                element_type=ElementType.enviornment,
                weight=mapper.get_env_weight(key=key),
            )
            for key in EnviornmentTypes
        }

        self.env_objects: dict[EnviornmentTypes,BaseEnviornment] = {}

        self._initialized  = True

    def get_env_element(self,key: EnviornmentTypes) -> BaseEnviornment:
        # return the object of the class. Can be used for rendering
        if key in self.env_objects.keys():
            return self.env_objects[key]

        else:
            obj = mapper.get_env_class(key=key)(self.window)
            self.env_objects[key] = obj
            return obj
    
    def get_current_count(self,key):
        return self.tracker[key].current_count

    def get_max_count(self,key: EnviornmentTypes):
        # return the max number of spawns for the given enviornment
        return int(self.tracker[key].weight * self.board_size)

    def update_evn_element_count(self, key: EnviornmentTypes, value: int):
        # update the number of elements of the enviornment type on the board
        self.tracker[key].current_count = value

    def current_and_max_all(self):
        return {
            key: {
                "current": tracker.current_count,
                "max": int(tracker.weight * self.board_size)
            }
            for key, tracker in self.tracker.items()
        }
