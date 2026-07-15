import random


from src.utils.mapper import mapper
from src.data_stores.tile import Tile
from src.manager.world import WorldManager
from src.data_stores.tick import EnviornmentTick

class EnviornmentGenerator:
    def __init__(
        self,
        spaces_on_x: int,
        spaces_on_y: int,
        process_rate: int,
        new_event_gen_rate: int,
        world_manager: WorldManager
    ):
        self.spaces_on_x: int = spaces_on_x
        self.spaces_on_y: int = spaces_on_y
        self.world_manager: WorldManager = world_manager

        # lets go for a queue approach
        self.process_queue: list[EnviornmentTick] = []
        self.coordinate_tracker: set[tuple[int]] = set()
        self.process_rate: int = process_rate
        self.new_event_gen_rate: int = new_event_gen_rate

    def process_tick(self):

        event_to_process = self.process_queue.pop(0)
        self.coordinate_tracker.remove(
            (event_to_process.x_cord,event_to_process.y_cord)
        )

        world_tile = self.world_manager.get_tile_information(
            x_cord=event_to_process.x_cord,
            y_cord=event_to_process.y_cord
        )

        if event_to_process.spawn_type == None:
            event_to_process.spawn_type = world_tile.env_tick()
        else:
            world_tile.env_tick(type_to_spawn=event_to_process.spawn_type)

        if event_to_process.spawn_type == None:
            # failed to spawn anything
            return
        else:    
            if event_to_process.growth_potential == 0:
                # the eye has grown as much as it can
                return
            
            elif event_to_process.growth_potential == None:
                # This is the eye. Need to determines how much the eye can spread
                event_to_process.growth_potential = random.randint(
                    *mapper.get_env_size(key=event_to_process.spawn_type)
                ) 

                if event_to_process.growth_potential == 0:
                    # the eye has decided not to spread
                    return
            
            
            if event_to_process.proc_randomness > 0:
                if random.random() > 0.25:
                    event_to_process.growth_potential += 2
                event_to_process.proc_randomness -= 1
            else:
                event_to_process.growth_potential -= 1

            # determine the directions to move towards
            directions = random.sample(
                ["up","down","left","right"], 
                random.randint(
                    *mapper.get_env_spread_direction_count(key=event_to_process.spawn_type)
                )
            )

            if (
                event_to_process.x_cord - 1 >= 0 
                and "up" in directions
                and (event_to_process.x_cord - 1, event_to_process.y_cord) not in self.coordinate_tracker
            ):
                # can move up
                self.coordinate_tracker.add((event_to_process.x_cord - 1, event_to_process.y_cord))
                self.process_queue.append(EnviornmentTick(
                    x_cord=event_to_process.x_cord - 1,
                    y_cord=event_to_process.y_cord,
                    proc_randomness=event_to_process.proc_randomness,
                    growth_potential=event_to_process.growth_potential,
                    spawn_type=event_to_process.spawn_type
                ))
                
            
            if (
                event_to_process.x_cord + 1 < self.spaces_on_x 
                and "down" in directions
                and (event_to_process.x_cord + 1, event_to_process.y_cord) not in self.coordinate_tracker
            ):
                # can move_down
                self.coordinate_tracker.add((event_to_process.x_cord + 1, event_to_process.y_cord))
                self.process_queue.append(EnviornmentTick(
                    x_cord=event_to_process.x_cord + 1,
                    y_cord=event_to_process.y_cord,
                    proc_randomness=event_to_process.proc_randomness,
                    growth_potential=event_to_process.growth_potential,
                    spawn_type=event_to_process.spawn_type
                ))

            if (
                event_to_process.y_cord - 1 >= 0 
                and "left" in directions
                and (event_to_process.x_cord, event_to_process.y_cord - 1) not in self.coordinate_tracker
            ):
                # can move left 
                self.coordinate_tracker.add((event_to_process.x_cord, event_to_process.y_cord - 1))
                self.process_queue.append(EnviornmentTick(
                    x_cord=event_to_process.x_cord,
                    y_cord=event_to_process.y_cord - 1,
                    proc_randomness=event_to_process.proc_randomness,
                    growth_potential=event_to_process.growth_potential,
                    spawn_type=event_to_process.spawn_type
                ))

            if (
                event_to_process.y_cord + 1 < self.spaces_on_y 
                and "right" in directions
                and (event_to_process.x_cord, event_to_process.y_cord + 1) not in self.coordinate_tracker
            ):
                # can move left 
                self.coordinate_tracker.add((event_to_process.x_cord, event_to_process.y_cord + 1))
                self.process_queue.append(EnviornmentTick(
                    x_cord=event_to_process.x_cord,
                    y_cord=event_to_process.y_cord + 1,
                    proc_randomness=event_to_process.proc_randomness,
                    growth_potential=event_to_process.growth_potential,
                    spawn_type=event_to_process.spawn_type
                ))

    def generate_ticks(self):
        choosen_rows = random.sample(range(self.spaces_on_y),self.new_event_gen_rate)

        for y_cord in choosen_rows:
            x_cord = random.randint(0,self.spaces_on_x - 1)

            if (x_cord,y_cord) in self.coordinate_tracker:
                # event already queued in location
                continue

            self.coordinate_tracker.add((x_cord,y_cord))
            self.process_queue.append(
                EnviornmentTick(
                    x_cord=x_cord,
                    y_cord=y_cord,
                    proc_randomness=random.randint(0,2)
                )
            )

    def process_loop(self):
        if len(self.process_queue) < self.process_rate:
            self.generate_ticks() # queue new events

        index = 0

        while index < self.process_rate and len(self.process_queue) > 0:
            self.process_tick()
            index += 1
