# This class will hold each individual tile/pixel
# This class will also handle the rendering of the tile, its state and interaction between
# the entities and enviornment present on it
import pygame
import random
from uuid import uuid4
from rich import print

from src.manager.entity import EntityTracker
from src.manager.enviornment import EnviornmentTracker
from src.utils.enums import EnviornmentTypes, EntityTypes, EntityFoodType

class Tile:
    def __init__(
        self,
        window,
        x_cord: int,
        y_cord: int,
        length: float,
        width: float,
        entity_tracker: EntityTracker,
        env_tracker: EnviornmentTracker
    ):
        self.x_cord: int = x_cord
        self.y_cord: int = y_cord
        self.length: float = length
        self.width: float = width
        self.window = window

        self.color: tuple[int] = (99, 81, 71)
        self._has_updated: bool = True

        # how likely each env type is to spawn on the current tile
        self.env_weights: dict[EnviornmentTypes,float] = {
            key:random.random()
            for key in EnviornmentTypes
        }

        # how likely each entity type is to spawn on the current tile
        self.entity_weight: dict[EntityTypes,float] = {
            key:random.random()
            for key in EntityTypes
        }
        
        # enviornment details
        self.current_enviornment: EnviornmentTypes | None = None
        self.env_tracker_instance: EnviornmentTracker = env_tracker
        # entity details
        self.entity_exists: bool = False
        self.entities_on_tile: dict[EntityFoodType,list[str]] = {
            key:[]
            for key in EntityFoodType
        }
        self.entity_tracker_instance: EntityTracker = entity_tracker

    def render(self):
        
        # if there is an evniornment then draw the enviornment 
        if self.current_enviornment != None:
            self.env_tracker_instance.get_env_element(self.current_enviornment).render(
                x_cord=self.x_cord,
                y_cord=self.y_cord,
                length=self.length,
                width=self.width
            )
        
        else:
            pygame.draw.rect(
                surface=self.window,
                color=self.color,
                rect=pygame.Rect(
                    self.x_cord,
                    self.y_cord,
                    self.length,
                    self.width
                )
            )

        # draw all the entities that are there on the current tile
        for entity_food_type,entity_id_list in self.entities_on_tile.items():
            for entity_id in entity_id_list:
                entity_instance = self.entity_tracker_instance.get_entity_instance(
                    entity_food_type=entity_food_type,
                    identifier=entity_id
                )

                if entity_instance == None:
                    continue

                entity_instance.render(
                    length=self.length,
                    width=self.width
                )
        
        self._has_updated = False
    
    def env_tick(self,type_to_spawn: EnviornmentTypes | None = None) -> None | EnviornmentTypes:
        # an enviornment event is triggered on this tile

        if type_to_spawn == None:
            # if this is the eye, then we will need to decide what to spawn
            type_to_spawn = random.choice(list(self.env_weights.keys()))

        if self.current_enviornment != None:
            # there is already an env on this tile
            self.env_weights[type_to_spawn] = min(self.env_weights[type_to_spawn] + 0.1, 1)
            return None # no further attempts needed
        else:
            # there is nothing here, we can attempt a spawn
            if (
                self.env_weights[type_to_spawn] >= 0.5
                and self.env_tracker_instance.get_current_count(key=type_to_spawn) < self.env_tracker_instance.get_max_count(key=type_to_spawn)
            ):
                # the weight to spawn is high enough and the max count is still not reached
                self.current_enviornment = type_to_spawn
                self.env_tracker_instance.update_evn_element_count(key=type_to_spawn,value=1)
                self.env_weights[type_to_spawn] = min(max(0,self.env_weights[type_to_spawn] - 0.1),0.3)
                self._has_updated = True # since we have updated the tile
                return type_to_spawn
            
            else:
                self.env_weights[type_to_spawn] = min(self.env_weights[type_to_spawn] + 0.1, 1)
                return None
    
    def entity_tick(self,type_to_spawn: EntityTypes | None = None) -> None | EntityTypes:
        if type_to_spawn == None:
            # this is the start point for the pack
            type_to_spawn = random.choice(list(self.entity_weight.keys()))
        
        # multiple entities can exist on a tile, but if any entity exists on the tile, 
        # the tile cannot spawn a new entity
        if self.entity_exists:
            # there is someone on this tile currently
            self.entity_weight[type_to_spawn] = min(self.entity_weight[type_to_spawn] + 0.1, 1)
            return None

        else:
            if (
                self.entity_weight[type_to_spawn] >= 0.5
                and self.entity_tracker_instance.get_current_count(type_to_spawn) < self.entity_tracker_instance.get_max_count(type_to_spawn)
            ):
                # mark the flags as true
                self.entity_exists = True 
                self._has_updated = True

                entity_id = str(uuid4())
                entity_food_type = self.entity_tracker_instance.register_entity(
                    identifier=entity_id,
                    key=type_to_spawn,
                    x_cord=self.x_cord,
                    y_cord=self.y_cord
                )

                self.entities_on_tile[entity_food_type].append(entity_id)
                self.entity_tracker_instance.update_entity_element_count(key=type_to_spawn,value=1)
                self.entity_weight[type_to_spawn] = min(max(0,self.entity_weight[type_to_spawn] - 0.1),0.3)
                return type_to_spawn
            
            else:
                self.entity_weight[type_to_spawn] = min(self.entity_weight[type_to_spawn] + 0.1, 1)
                return None


    @property
    def has_updated(self):
        return self._has_updated
        
    @has_updated.setter
    def has_updates(self,value:bool):
        if value not in (True, False):
            raise Exception(f"Incorrect value passed for tile has_updated - {value}")
        self._has_updated = value