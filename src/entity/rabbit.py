import random


from src.entity.base import BaseEntity
from src.utils.enums import EntityFoodType, Direction


class RabbitEntity(BaseEntity):
    def __init__(self, window, x_cord, y_cord):
        color_choice = random.choice([
            {"body": (235, 230, 222),"head": (205, 196, 185)},
            {"body": (245, 245, 245),"head": (215, 215, 215)},
            {"body": (186, 145, 106),"head": (143, 104, 74)},
            {"body": (185, 187, 190),"head": (140, 144, 150)},
            {"body": (228, 216, 196),"head": (188, 168, 144)},
        ])
        super().__init__(
            window=window,
            x_cord=x_cord,
            y_cord=y_cord,
            health=10,
            hunger=10,
            thirst=10,
            movement_speed=1,
            food_type=EntityFoodType.herbivore,
            hunger_restore=2,
            thirst_restore=0,
            scale_entity_width=1,
            scale_entity_length=0.5,
            body_color=color_choice["body"],
            head_color=color_choice["head"],
            direction_facing=random.choice(list(Direction)),
        )
