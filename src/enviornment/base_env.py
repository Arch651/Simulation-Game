# base config class of an enviornment type
import pygame

from src.utils.enums import (
    EnvTickType,
    TopEnviornmentTypes,
    EnviornmentalAttributes, 
)


class EnviornmentBase:
    def __init__(
        self,
        window: pygame.Surface,
        color: tuple[int],
        hunger_restore: int,
        thirst_restore: int,
        top_layers: dict[EnviornmentalAttributes,list[TopEnviornmentTypes]]
    ):
        self.window: pygame.Surface = window
        self.color: tuple[int] = color
        self.hunger_restore: int = hunger_restore
        self.thirst_restore: int = thirst_restore
        self.top_layers: dict[
            EnviornmentalAttributes,dict[
                EnvTickType,
                list[TopEnviornmentTypes]
        ]] = top_layers

    def render(self,
        position_x: int,
        position_y: int,
        length: int,
        height: int,
        full: bool = True
    ):
        pygame.draw.rect(
            surface=self.window,
            color=self.color,
            rect=pygame.Rect(
                position_x,
                position_y,
                length,
                height
            ),
            width=0 if full else 1,
        )
    
    def fetch_possible_top_layers(
        self,
        environmental_attribute: EnviornmentalAttributes,
        enviornmental_tick_type: EnvTickType | None
    ) -> list:
        """For a given enviornmental attribute event and a given enviornmental tick
        type, return the possible enviornmental types that can be generated
        """
        if enviornmental_tick_type != None:
            return self.top_layers.get(environmental_attribute,{}).get(enviornmental_tick_type,[])

        else:
            all_possible_top_layers =  []
            all_possible_top_layers += self.top_layers.get(environmental_attribute,{}).get(EnvTickType.active,[])
            all_possible_top_layers += self.top_layers.get(environmental_attribute,{}).get(EnvTickType.passive,[])

            return all_possible_top_layers

        