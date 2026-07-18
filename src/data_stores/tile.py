"""
This class will hold the tile entity that is responsible for storing the details about the enviornment
"""

import pygame
import random
from rich import print

from src.utils.enums import (
    EnvTickType,
    TopEnviornmentTypes,
    BaseEnviornmentTypes,
    EnviornmentalAttributes,
)
from src.utils.mapper import mapper
from src.manager.settings import GlobalSettings
from src.manager.enviornment import EnviornmentTracker


class Tile:
    def __init__(
        self,
        window: pygame.Surface,
        identifier: tuple[int],
        position_x: int,
        position_y: int,
        settings: GlobalSettings,
        enviornment_tracker: EnviornmentTracker,
    ):
        self.identifier: tuple[int] = identifier
        self.position_x: int = position_x
        self.position_y: int = position_y
        self.window: pygame.Surface = window

        # passed from the world instead of building a new one everytime
        self.settings: GlobalSettings = settings
        self.enviornment_tracker: EnviornmentTracker = enviornment_tracker

        # now lets calculate its enviornmental attributes
        self.enviornmental_attributes: dict[EnviornmentalAttributes, float] = {
            key: random.random() for key in EnviornmentalAttributes
        }

        # this variable will store what is enviornment is there on the tile currently
        self.enviornment_layers: dict[
            int, TopEnviornmentTypes | BaseEnviornmentTypes
        ] = {}

        self.base_color: tuple[int] = (0,0,0) #(99, 81, 71)
        self.should_render: bool = True

    
    def process_env_tick(
        self,
        enviornment_attribute: EnviornmentalAttributes,
        env_tick_type: EnvTickType,
        enviornment_to_spawn: BaseEnviornmentTypes | TopEnviornmentTypes | None
    ) -> BaseEnviornmentTypes | TopEnviornmentTypes | None:
        
        if enviornment_to_spawn == None:
            if self.enviornment_layers.get(0) == None:
                # need to determine the base layer to spawn
                enviornment_to_spawn = random.choice(
                    mapper.get_base_env_for_env_attributes(key=enviornment_attribute)
                )
            else:
                # need to determine the top layer to spawn
                possible_top_layer = self.enviornment_tracker.get_env_element(
                    self.enviornment_layers.get(0)
                ).fetch_possible_top_layers(
                    environmental_attribute=enviornment_attribute,
                    enviornmental_tick_type=env_tick_type
                )

                if len(possible_top_layer) == 0:
                    # no possible top layers found for the provided combination
                    return None

                enviornment_to_spawn = random.choice(possible_top_layer)

        if (
            self.enviornmental_attributes[enviornment_attribute] >= 0.2
            and self.enviornment_tracker.get_current_count(enviornment_to_spawn) < self.enviornment_tracker.get_max_count(
                enviornment_to_check=enviornment_to_spawn,
                base_layer=self.enviornment_layers.get(0)
            )
        ):
            # if it is possible to spawn the selected env
            key = max(self.enviornment_layers.keys()) + 1 if len(self.enviornment_layers.keys()) != 0 else 0
            self.enviornment_layers[key] = enviornment_to_spawn
            return enviornment_to_spawn
        elif (
            enviornment_attribute == EnviornmentalAttributes.fertility
            and self.enviornmental_attributes[enviornment_attribute] < 0.15
            and self.enviornment_layers.get(0) == None
            and self.enviornment_tracker.get_current_count(BaseEnviornmentTypes.barren) < self.enviornment_tracker.get_max_count(BaseEnviornmentTypes.barren)
        ):
            # in case the event was to grow a grass layer but the fertility is too low
            # the land can convert into a barrent land
            self.enviornment_layers[0] = BaseEnviornmentTypes.barren
            return BaseEnviornmentTypes.barren
        else:
            return None
    

    def env_tick(
        self,
        enviornment_attribute: EnviornmentalAttributes,
        env_tick_type: EnvTickType,
        growth_direction: int = 1,
        enviornment_to_spawn: BaseEnviornmentTypes | TopEnviornmentTypes | None = None,
    ) -> BaseEnviornmentTypes | TopEnviornmentTypes | None:

        spawned_env_type = None

        if (
            (
                enviornment_to_spawn in list(TopEnviornmentTypes) and (
                    self.enviornment_layers.get(0) == None
                    or enviornment_to_spawn not in self.enviornment_tracker.get_env_element(
                        self.enviornment_layers.get(0)
                    ).fetch_possible_top_layers(
                        environmental_attribute=enviornment_attribute,
                        enviornmental_tick_type=None
                    )
                )
            )
            or (self.enviornment_layers.get(0) != None and self.enviornment_layers.get(1) != None)
            or growth_direction not in (-1,1)
           
        ):
            # all sorts of immediate failure condition
            return spawned_env_type   

        if (
            env_tick_type == EnvTickType.passive
            and enviornment_to_spawn in list(BaseEnviornmentTypes)
            and self.enviornment_layers.get(0) != None
        ):
            # there is a baseEnv spawn even of passive kind and the current block only has a base layer
            # we will remove the associated event and let it continue 
            enviornment_to_spawn = None
        
        # now we will calibrate the growth factors
        if growth_direction == -1:
            self.enviornmental_attributes[enviornment_attribute] = max(
                0, self.enviornmental_attributes[enviornment_attribute] - 0.1
            )

        elif growth_direction == 1:
            self.enviornmental_attributes[enviornment_attribute] = min(
                1,self.enviornmental_attributes[enviornment_attribute] + 0.1
            )
        
        spawned_env_type = self.process_env_tick(
            enviornment_attribute=enviornment_attribute,
            env_tick_type=env_tick_type,
            enviornment_to_spawn=enviornment_to_spawn
        )

        if spawned_env_type != None:
            self.should_render = True
            self.enviornment_tracker.update_evn_element_count(
                key=spawned_env_type,
                value=1
            )

        return spawned_env_type

    def render(self):

        if self.enviornment_layers.get(1) != None:
            # if there is a top layer, then ask the enviornment tracker to do the render
            env_element_instance = self.enviornment_tracker.get_env_element(
                key=self.enviornment_layers[1]
            )

            env_element_instance.render(
                position_x=self.position_x,
                position_y=self.position_y,
                length=self.settings.scale_along_x,
                height=self.settings.scale_along_y,
            )

            self.enviornment_tracker.get_env_element(
                key=self.enviornment_layers[0]
            ).render(
                position_x=self.position_x,
                position_y=self.position_y,
                length=self.settings.scale_along_x,
                height=self.settings.scale_along_y,
                full=False
            )

        elif self.enviornment_layers.get(0) != None:
            # if there is a base layer, then ask the enviornment tracker to do the render
            env_element_instance = self.enviornment_tracker.get_env_element(
                key=self.enviornment_layers[0]
            )

            env_element_instance.render(
                position_x=self.position_x,
                position_y=self.position_y,
                length=self.settings.scale_along_x,
                height=self.settings.scale_along_y,
            )

        else:
            pygame.draw.rect(
                self.window,
                color=self.base_color,
                rect=pygame.Rect(
                    self.position_x,
                    self.position_y,
                    self.settings.scale_along_x,
                    self.settings.scale_along_y,
                ),
            )

        self.should_render = False
