import random
import pygame
from abc import ABC,abstractmethod

from src.utils.enums import (
    Direction,
    EntityTypes,
    EntityActions,
    EntityFoodType, 
)

class BaseEntity(ABC):
    def __init__(
        self,
        world,
        window,
        unique_id: str,
        tile_identifier: tuple[int],
        etype: EntityTypes,
        x_cord: int,
        y_cord: int,
        health: int,
        hunger: int,
        thirst: int,
        movement_speed: int,
        food_type: EntityFoodType,
        hunger_restore: int,
        thirst_restore: int,
        scale_entity_width: float,
        scale_entity_length: float,
        body_color: tuple[int],
        head_color: tuple[int],
        direction_facing: Direction
    ):
        
        self.unique_id: str = unique_id
        self.tile_identifier: tuple[int] = tile_identifier
        self.etype: EntityTypes = etype

        # current position and things that will be needed for rendering
        self.window = window
        self.world = world
        self.x_cord: int = x_cord
        self.y_cord: int = y_cord
        self.scale_entity_width: float = scale_entity_width
        self.scale_entity_length: float = scale_entity_length
        self.body_color: tuple[int] = body_color
        self.head_color: tuple[int] = head_color
        self.direction_facing: Direction = direction_facing


        # every 1 in a 100 entity that spawns can be a beefy entity
        # a beefy entity has twice the health and restores twice the hunger and thirst
        # it will also be twice as fast
        beefy_entity: bool = False if random.random() < 0.99 else True 
        
        # max_stats
        self.max_health: int = health if not beefy_entity else 2 * health
        self.max_hunger: int = hunger
        self.max_thirst: int = thirst
        self.hunger_restore: int = hunger_restore if not beefy_entity else 2 * hunger_restore
        self.thirst_restore: int = thirst_restore if not beefy_entity else 2 * thirst_restore
        self.max_movement_speed: int = movement_speed if not beefy_entity else 2 * movement_speed
        self.food_type: EntityFoodType = food_type

        # current stats
        self.current_health: int = self.max_health
        self.current_hunger: int = self.max_hunger
        self.current_thirst: int = self.max_thirst

        # action related variable
        self.current_action: EntityActions = EntityActions.idle
        self.under_threat: bool = False
        

    def render(self, length: int, width: int):
        # this will be fun as i dont want an entity to just cover the entire pixel
        entity_length = None
        entity_width = None
        offset_length = 0
        offset_width = 0

        if self.direction_facing in (Direction.up,Direction.down):
            # determine what is the length of the pixel
            entity_length = length * self.scale_entity_length
            entity_width = width * self.scale_entity_width

        elif self.direction_facing in (Direction.left, Direction.right):
            # determine what is the length of the pixel
            entity_length = width * self.scale_entity_width
            entity_width = length * self.scale_entity_length

        offset_length = (length - entity_length) // 2
        offset_width = (width - entity_width) // 2

        # draw the body
        body_rect_object = pygame.Rect(
            self.x_cord + offset_length,
            self.y_cord + offset_width,
            entity_length,
            entity_width
        )


        pygame.draw.rect(surface=self.window, color=self.body_color, rect=body_rect_object)

        # draw the head
        if self.direction_facing == Direction.up:
            head_rect_object = pygame.Rect(
                self.x_cord + offset_length,
                self.y_cord + offset_width,
                entity_length,
                entity_width // 2
            )
        elif self.direction_facing == Direction.down:
            head_rect_object = pygame.Rect(
                (self.x_cord + offset_length),
                (self.y_cord + offset_width) + (entity_width // 2),
                entity_length,
                (entity_width // 2)
            )
        elif self.direction_facing == Direction.left:
            head_rect_object = pygame.Rect(
                self.x_cord + offset_length,
                self.y_cord + offset_width,
                entity_length // 2,
                entity_width
            )
        elif self.direction_facing == Direction.right:
            head_rect_object = pygame.Rect(
                (self.x_cord + offset_length) + (entity_length // 2),
                self.y_cord + offset_width,
                (entity_length // 2),
                entity_width
            )

        pygame.draw.rect(surface=self.window, color=self.head_color, rect=head_rect_object)
        pygame.draw.rect(surface=self.window, color=(0,0,0), rect=body_rect_object,width=1)
    
    def decide_action(self) -> bool:
        """
        Decide what action to perform in the current cycle.

        All entities will have access to the following actions
            - idle --> do nothing, this will result in a false being returned
            - eat --> consume food in order to increase its hunger points
            - drink --> consume water in order to increase its thirst points
            - wander --> choose a random point in front of it to move to
            - escape --> if under threat, then try to escape
            - chase --> move towards food
            - turn --> change its direction

        Args:
            None
        
        Returns: 
            True if an action is to be performed else a False
        """
        # TODO: will need to implement a NxN matrix search around the entity
        # actions such as chase, escape will depend on that

        possible_actions: list[EntityActions] = [
            EntityActions.wander,
            # EntityActions.turn,
            # EntityActions.idle
        ]

        # if self.current_hunger < self.max_hunger:
        #     possible_actions.append(EntityActions.eat)
        
        # if self.current_thirst < self.max_thirst:
        #     possible_actions.append(EntityActions.drink)


        self.current_action = random.choice(possible_actions)

        if self.current_action == EntityActions.idle:
            return False
        else:
            return True
        

    def passive_action(self):
        if self.current_hunger > 0 and self.current_health != 0:
            # every hunger point restores 2 health
            self.current_health = min(self.current_health + 2, self.max_health)
            self.current_hunger -= 1
        
        if self.current_hunger == 0:
            # stealing this from minecraft, but every tick that the entity 
            # is completely hungry it looses one health point
            self.current_health = max(self.current_health - 1, 0)

        if self.current_health == 0:
            current_tile = self.world.get_tile_information(
                x_cord=self.tile_identifier[0],
                y_cord=self.tile_identifier[1]
            )

            current_tile.entities_on_tile[self.food_class].remove(self.unique_id) # remove itself from the tile
            current_tile.has_updated = True

        

    @abstractmethod
    def perform_action(self):
        # perform the decided action
        # once we are done with performing the choosen action, we set it back to idle
        self.current_action = EntityActions.idle

    def turn(self):
        self.direction_facing = random.choice([
            d for d in Direction if d != self.direction_facing
        ])

        self.world.get_tile_information(
            x_cord=self.tile_identifier[0],
            y_cord=self.tile_identifier[1]
        ).has_updated = True

    @property
    def food_class(self):
        return self.food_type
    
    @property
    def health(self):
        return self.current_health
    
    @health.setter
    def health(self,value: int):
        self.current_health -= value

if __name__ == "__main__":

    running = True

    x_cord = 200
    y_cord = 100
    length = 750
    width = 500
    window = pygame.display.set_mode((1000,800))

    entity = BaseEntity(
        window=window,
        x_cord=x_cord,
        y_cord=y_cord,
        health=10,
        hunger=10,
        thirst=10,
        movement_speed=1,
        food_type=EntityFoodType.herbivore,
        hunger_restore=1,
        thirst_restore=1,
        scale_entity_length=1,
        scale_entity_width=1,
        body_color=(0,255,0),
        direction_facing=Direction.down
    )

    clock = pygame.time.Clock()

    window.fill((255,255,255))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        pygame.draw.rect(
            window,
            (255,0,0),
            (
                x_cord,
                y_cord,
                length,
                width
            )
        )
        entity.render(
            length=length,
            width=width
        )

        pygame.display.flip()
        clock.tick(30)