# i just want to get one entity to spawn first
# this class is only responsible for generating new entities

import random
from rich import print

from src.utils.mapper import mapper
from src.data_stores.tile import Tile
from src.manager.enviornment_world import EnviornmentWorldManager
from src.data_stores.tick import EntityTick


class EntityGenerator:
    def __init__(
        self,
        spaces_on_x: int,
        spaces_on_y: int,
        process_rate: int,
        new_entity_gen_rate: int,
        world_manager: EnviornmentWorldManager
    ):
        self.spaces_on_x: int = spaces_on_x
        self.spaces_on_y: int = spaces_on_y
        self.world_manager: EnviornmentWorldManager = world_manager

        # queue details
        self.process_queue: list[EntityTick] = []
        self.coordinate_tracker: set[tuple[int]] = set()
        self.process_rate: int = process_rate
        self.new_entity_gen_rate: int = new_entity_gen_rate

    def process_tick(self):
        event_to_process = self.process_queue.pop(0)
        self.coordinate_tracker.remove(
            (event_to_process.x_cord, event_to_process.y_cord)
        )

        world_tile = self.world_manager.get_tile_information(
            x_cord=event_to_process.x_cord,
            y_cord=event_to_process.y_cord
        )

        if event_to_process.spawn_type == None:
            # this is the first entity in this pack
            event_to_process.spawn_type = world_tile.entity_tick()
        else:
            world_tile.entity_tick(type_to_spawn=event_to_process.spawn_type)

        if event_to_process.spawn_type == None:
            # spawning an entity has failed
            return
        else:
            if event_to_process.pack_size == 0:
                # the entire pack has been spawned
                return

            elif event_to_process.pack_size == None:
                # this is the first entity in this pack. Need to determine the pack size
                event_to_process.pack_size = random.randint(
                    *mapper.get_entity_pack_size(event_to_process.spawn_type)
                )

                if event_to_process.pack_size == 0:
                    # the pack has stopped spawning more
                    return

            # determine all the sides available to continue spawing and then choose one
            possible_direction = []
            if event_to_process.x_cord + 1 < self.spaces_on_x:
                possible_direction.append(
                    (event_to_process.x_cord + 1, event_to_process.y_cord)
                )
            if event_to_process.x_cord - 1 >= 0:
                possible_direction.append(
                    (event_to_process.x_cord - 1, event_to_process.y_cord)
                )
            if event_to_process.y_cord + 1 < self.spaces_on_y:
                possible_direction.append(
                    (event_to_process.x_cord, event_to_process.y_cord + 1)
                )
            if event_to_process.y_cord - 1 >= 0:
                possible_direction.append(
                    (event_to_process.x_cord, event_to_process.y_cord - 1)
                )

            possible_direction = [d for d in possible_direction if d not in self.coordinate_tracker]

            if len(possible_direction) > 0:
                choosen_direction = random.choice(possible_direction)    
                self.coordinate_tracker.add(choosen_direction)
                self.process_queue.append(
                    EntityTick(
                        x_cord=choosen_direction[0],
                        y_cord=choosen_direction[1],
                        pack_size=event_to_process.pack_size - 1,
                        spawn_type=event_to_process.spawn_type
                    )
                )


    def generate_ticks(self):
        choosen_rows = random.sample(range(self.spaces_on_y), self.new_entity_gen_rate)

        for y_cord in choosen_rows:
            x_cord = random.randint(0, self.spaces_on_x - 1)

            if (x_cord, y_cord) in self.coordinate_tracker:
                # event already queued in location
                continue

            self.coordinate_tracker.add((x_cord, y_cord))
            self.process_queue.append(EntityTick(x_cord=x_cord, y_cord=y_cord))

    def process_loop(self):
        if len(self.process_queue) < self.process_rate:
            self.generate_ticks()  # queue new events

        index = 0

        while index < self.process_rate and len(self.process_queue) > 0:
            self.process_tick()
            index += 1
