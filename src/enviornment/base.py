# base config class of an enviornment type
import pygame


class BaseEnviornment:
    def __init__(
        self,
        window,
        color: tuple[int],
        hunger_restore: int = 0,
        thirst_restore: int = 0,
    ):
        self.color: tuple[int] = color
        self.hunger_restore: int = hunger_restore
        self.thirst_restore: int = thirst_restore
        self.window = window

    def render(self,
        x_cord: int,
        y_cord: int,
        length: int,
        width: int
    ):
        pygame.draw.rect(
            surface=self.window,
            color=self.color,
            rect=pygame.Rect(
                x_cord,
                y_cord,
                length,
                width
            )
        )

        