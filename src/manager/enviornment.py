# store a tracker for enviornment elements
from pygame import Surface
from itertools import chain


from src.utils.mapper import mapper
from src.data_stores.tracker import Tracker
from src.enviornment.base_env import EnviornmentBase
from src.utils.enums import ElementType, TopEnviornmentTypes, BaseEnviornmentTypes


class EnviornmentTracker:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, window: Surface, board_size: int):
        if self._initialized:
            return

        self.window: Surface = window
        self.board_size: int = board_size
        self.tracker: dict[BaseEnviornmentTypes | TopEnviornmentTypes, Tracker] = {
            key: Tracker(
                element_type=ElementType.enviornment,
                weight=mapper.get_env_weight(key=key),
            )
            for key in chain(BaseEnviornmentTypes, TopEnviornmentTypes)
        }

        self.env_objects: dict[
            BaseEnviornmentTypes | TopEnviornmentTypes, EnviornmentBase
        ] = {}

        self._initialized = True

    def get_env_element(
        self, key: BaseEnviornmentTypes | TopEnviornmentTypes
    ) -> EnviornmentBase:
        # return the object of the class. Can be used for rendering
        if key in self.env_objects.keys():
            return self.env_objects[key]

        else:
            obj = mapper.get_env_class(key=key)(self.window)
            self.env_objects[key] = obj
            return obj

    def get_current_count(
        self, 
        key: BaseEnviornmentTypes | TopEnviornmentTypes
    ):
        return self.tracker[key].current_count

    def get_max_count(
        self, 
        enviornment_to_check: BaseEnviornmentTypes | TopEnviornmentTypes,
        base_layer: BaseEnviornmentTypes | None = None
    ):
        # return the max number of spawns for the given enviornment
        if enviornment_to_check in list(TopEnviornmentTypes) and base_layer == None:
            raise Exception(f'No base layer provided wile fetching max count for - {enviornment_to_check}')
        
        if base_layer == None:
            return int(self.tracker[enviornment_to_check].weight * self.board_size)
        
        else:
            return int (
                (self.tracker[base_layer].weight * self.board_size) * self.tracker[enviornment_to_check].weight
            )

    def update_evn_element_count(
        self, key: BaseEnviornmentTypes | TopEnviornmentTypes, value: int
    ):
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