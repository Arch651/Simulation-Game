import random
from rich import print

from src.entity.base import BaseEntity
from src.utils.enums import (
    EntityFoodType, Direction, EntityActions, EntityTypes
)


class RabbitEntity(BaseEntity):
    def __init__(
            self, 
            world,
            window,
            tile_identifier: tuple[int], 
            unique_id: str,
            x_cord: int, 
            y_cord: int,
        ):
        color_choice = random.choice([
            {"body": (235, 230, 222),"head": (205, 196, 185)},
            {"body": (245, 245, 245),"head": (215, 215, 215)},
            {"body": (186, 145, 106),"head": (143, 104, 74)},
            {"body": (185, 187, 190),"head": (140, 144, 150)},
            {"body": (228, 216, 196),"head": (188, 168, 144)},
        ])
        super().__init__(
            unique_id=unique_id,
            tile_identifier=tile_identifier,
            etype=EntityTypes.rabbit,
            window=window,
            x_cord=x_cord,
            y_cord=y_cord,
            world=world,
            health=10,
            hunger=100,
            thirst=10,
            movement_speed=2,
            food_type=EntityFoodType.herbivore,
            hunger_restore=2,
            thirst_restore=0,
            scale_entity_width=1,
            scale_entity_length=0.5,
            body_color=color_choice["body"],
            head_color=color_choice["head"],
            direction_facing=random.choice(list(Direction)),
        )
    
    def perform_action(self):
        if self.current_action == EntityActions.turn:
            self.turn()
        
        elif self.current_action == EntityActions.wander:
            if self.current_hunger > 0:
                if self.direction_facing == Direction.up:
                    possible_y = [
                        i for i in range(
                            max(0,self.tile_identifier[1] - self.max_movement_speed),
                            self.tile_identifier[1]
                        )
                    ]
                    if len(possible_y) > 0:
                        new_tile_identifier = (self.tile_identifier[0],random.choice(possible_y))
                    else:
                        new_tile_identifier = self.tile_identifier
                
                elif self.direction_facing == Direction.down:
                    possible_y = [
                        i for i in range(
                            self.tile_identifier[1],
                            min(self.world.max_width,self.tile_identifier[1] + self.max_movement_speed) + 1
                        ) if i != self.world.max_width
                    ]

                    if len(possible_y) > 0:
                        new_tile_identifier = (self.tile_identifier[0],random.choice(possible_y))
                    else:
                        new_tile_identifier = self.tile_identifier

                elif self.direction_facing == Direction.left:
                    possible_x = [
                        i for i in range(
                            max(0,self.tile_identifier[0] - self.max_movement_speed),
                            self.tile_identifier[0]
                        )
                    ]

                    if len(possible_x) > 0:
                        new_tile_identifier = (random.choice(possible_x),self.tile_identifier[1])
                    else:
                        new_tile_identifier = self.tile_identifier
                
                elif self.direction_facing == Direction.right:
                    possible_x = [
                        i for i in range(
                            self.tile_identifier[0],
                            min(self.world.max_length,self.tile_identifier[0] + self.max_movement_speed) + 1
                        ) if i != self.world.max_length
                    ]

                    if len(possible_x) > 0:
                        new_tile_identifier = (random.choice(possible_x),self.tile_identifier[1])
                    else:
                        new_tile_identifier = self.tile_identifier

                # now the entity needs to remove itself from the current tile and move itself to the new time
                if new_tile_identifier != self.tile_identifier:

                    old_tile = self.world.get_tile_information(
                        x_cord=self.tile_identifier[0],
                        y_cord=self.tile_identifier[1]
                    )
                    old_tile.entities_on_tile[self.food_class].remove(self.unique_id)
                    old_tile.has_updated = True

                    new_tile = self.world.get_tile_information(
                        x_cord=new_tile_identifier[0],
                        y_cord=new_tile_identifier[1]
                    )
                    
                    new_tile.entities_on_tile[self.food_class].append(self.unique_id)
                    new_tile.has_updated = True

                    self.current_hunger = max(0,self.current_hunger - (abs(new_tile_identifier[0] - self.tile_identifier[0]) + abs(new_tile_identifier[1] - self.tile_identifier[1]))) # every block moved will use one hunger
                    
                    self.tile_identifier = new_tile_identifier
                    self.x_cord = new_tile.x_cord
                    self.y_cord = new_tile.y_cord

                else:
                    self.turn()


        return super().perform_action()
