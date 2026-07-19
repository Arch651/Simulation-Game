# Create a entity world on top of the base world.
# The entity world will need access to the world below for the following actions
# - Calculate the tile on which the current entity is
# - Update the state of the tile under the entity
import pygame
import random

from src.utils.enums import (
    EntityTypes,
)
from src.data_stores.tick import EntityTick
from src.manager.entity import EntityTracker
from src.manager.settings import GlobalSettings
from src.manager.enviornment_world import EnviornmentWorldManager

class EntityWorldManager:
    _instance = None
    _initialized = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(
        self,
        window: pygame.Surface,
        settings: GlobalSettings,
        enviornment_world: EnviornmentWorldManager,
    ):
        
        if self._initialized:
            return
        
        self.window: pygame.Surface = window
        self.settings: GlobalSettings = settings
        self.enviornment_world: EnviornmentWorldManager = enviornment_world
        self.entity_tracker: EntityTracker = EntityTracker(
            window=self.window,
            board_size=self.settings.board_size_entity
        )

        self.entity_grid: list[list[None | EntityTypes]] = [
            [None] * self.settings.game_area_x_length
            for _ in range(self.settings.game_area_y_length)
        ]
        
        self.entity_tick_queue: list[EntityTick] = []
        self.coordinate_with_event: set[tuple[int]] = set()

        self._initialized = True

    def render_entity(self) -> None: ...

    def process_entity_tick(self):
        event_to_process = self.entity_tick_queue.pop(0)
        self.coordinate_with_event.remove(
            (event_to_process.x_cord,event_to_process.y_cord)
        )

        if (
            self.entity_grid[event_to_process.y_cord][event_to_process.x_cord] != None
        ):
            # things that will cause immediate faiure in the spawn cycle
            return 
        
        



    def process_loop(self) -> None:
        """
        This function is responsible for the spawning of new entities only.
        All entity actions will be governed by a different set of function
        """
        if len(self.entity_tick_queue) < self.settings.entity_tick_process_rate:
            for y_cord in random.sample(range(self.settings.game_area_y_length),self.settings.entity_tick_generate_rate):
                x_cord = random.randint(0,self.settings.game_area_x_length - 1)

                coord_identifier = (x_cord,y_cord)

                if coord_identifier in self.coordinate_with_event:
                    continue

                self.coordinate_with_event.add(coord_identifier)
                self.entity_tick_queue.append(
                    EntityTick(
                        x_cord=x_cord,
                        y_cord=y_cord,
                    )
                )
        
        # process the existing events
        counter = 0
        while (
            counter < self.settings.entity_tick_process_rate
            and len(self.entity_tick_queue) > 0
        ):
            self.process_entity_tick()
            counter += 1