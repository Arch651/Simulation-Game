# store the tracking information for entities
from src.utils.enums import (
    EntityTypes,
    ElementType,
    EntityFoodType
)
from src.utils.mapper import mapper
from src.entity.base import BaseEntity
from src.data_stores.tracker import Tracker

class EntityTracker:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        window,
        board_size: int
    ):
        if self._initialized:
            return

        self.window = window
        self.board_size: int = board_size
        self.tracker: dict[EntityTypes,Tracker] = {
            key: Tracker(
                element_type=ElementType.entity,
                weight=mapper.get_entity_weight(key=key)
            )
            for key in EntityTypes
        }    

        self.entity_objects: dict[EntityFoodType,dict[str,BaseEntity]] = {
            key:{}
            for key in EntityFoodType
        }

        self._initialized = True

    def get_current_count(self,key: EntityTypes):
        return self.tracker[key].current_count
    
    def get_max_count(self,key: EntityTypes):
        # return the max number of spawns for the given entity
        return int(self.tracker[key].weight * self.board_size)

    def update_entity_element_count(self, key: EntityTypes, value: int):
        # update the number of elements of the entity type on the board
        self.tracker[key].current_count = value

    def remove_dead_entities(self):

        new_mapping = {}
        for entity_food_type,entities in self.entity_objects.items():
            new_mapping[entity_food_type] = {}
            for identifier,entity in entities.items():
                if entity.health <= 0:
                    self.tracker[entity.etype].current_count = -1
                    continue

                new_mapping[entity_food_type][identifier] = entity
        
        self.entity_objects = new_mapping
    
    def register_entity(
        self,
        identifier: str,
        tile_identifier: tuple[int],
        key: EntityTypes,
        x_cord: int,
        y_cord: int,
        world
    ) -> EntityFoodType:
        # spawn and register a new entity. return the food class for the spawned entity
        
        new_entity = mapper.get_entity_class(key=key)(
            unique_id=identifier,
            tile_identifier=tile_identifier,
            window=self.window,
            x_cord=x_cord,
            y_cord=y_cord,
            world=world
        )
        self.entity_objects[new_entity.food_class][identifier] = new_entity

        return new_entity.food_class

    def unregister_entity(
        self,
        identifier: str,
        entity_food_type: EntityFoodType
    ):
        # remove an entity from the tracker when it dies
        self.entity_objects[entity_food_type].pop(identifier,None)

    def get_entity_instance(
        self,
        entity_food_type: EntityFoodType,
        identifier: str
    ) -> BaseEntity | None:

        return self.entity_objects[entity_food_type].get(identifier,None)
