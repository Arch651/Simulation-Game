import random
import pygame


from src.utils.enums import (
    EnvTickType,
    EnviornmentalAttributes,
)
from src.utils.mapper import mapper
from src.data_stores.tile import Tile
from src.manager.settings import GlobalSettings
from src.data_stores.tick import EnviornmentTick
from src.manager.enviornment import EnviornmentTracker


class WorldManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        window: pygame.Surface,
        settings: GlobalSettings,
    ):
        if self._initialized:
            return

        self.window: pygame.Surface = window
        self.settings: GlobalSettings = settings
        self.enviornment_tracker: EnviornmentTracker = EnviornmentTracker(
            window=self.window, board_size=self.settings.board_size_enviornment
        )

        self.tile_grid: list[list[Tile]] = []

        self.env_tick_queue: list[EnviornmentTick] = []
        self.tile_with_event_tracker: set[tuple[int]] = set()

        self._initialized = True

    def generate_game_world(self):
        # generate the tiles that will handle the game logic at a pixel
        for identifier_y in range(self.settings.tiles_along_y):
            res = []
            for identifier_x in range(self.settings.tiles_along_x):
                res.append(
                    Tile(
                        window=self.window,
                        identifier=(identifier_x, identifier_y),
                        position_x=(
                            self.settings.game_area_x_offset
                            + (identifier_x * self.settings.scale_along_x)
                        ),
                        position_y=(
                            self.settings.game_area_y_offset
                            + (identifier_y * self.settings.scale_along_y)
                        ),
                        settings=self.settings,
                        enviornment_tracker=self.enviornment_tracker,
                    )
                )
            self.tile_grid.append(res)

    def render_tile(self) -> None:
        for row in self.tile_grid:
            for tile in row:
                if not tile.should_render:
                    continue
                tile.render()

    def process_env_tick(self):
        # fetching the event that needs to be processed
        event_to_process = self.env_tick_queue.pop(0)
        self.tile_with_event_tracker.remove(
            (event_to_process.position_x, event_to_process.position_y)
        )

        tile = self.tile_grid[event_to_process.position_y][event_to_process.position_x]


        # decide the kind of event that we want to trigger
        if event_to_process.tick_type == EnvTickType.active:
            # this is the eye of the virus
            event_to_process.enviornment_attribute = random.choice(
                list(EnviornmentalAttributes)
            )

            event_to_process.enviornment_spawn_type = tile.env_tick(
                growth_direction=random.choice([-1,1]),
                enviornment_attribute=event_to_process.enviornment_attribute,
                env_tick_type=event_to_process.tick_type
            )

        else:
            event_to_process.enviornment_spawn_type = tile.env_tick(
                enviornment_attribute=event_to_process.enviornment_attribute,
                enviornment_to_spawn=event_to_process.enviornment_spawn_type,
                env_tick_type=event_to_process.tick_type
            )

        if event_to_process.enviornment_spawn_type == None:
            # failed to spawn anything
            return
        else:
            if event_to_process.spread_step_count == 0:
                # max spread reached
                return
            elif event_to_process.spread_step_count == None:
                # this is the eye, we need to determine a growth potential
                event_to_process.spread_step_count = random.randint(
                    *mapper.get_env_size(event_to_process.enviornment_spawn_type)
                )

                if event_to_process.spread_step_count == 0:
                    # the eye has decided not to spread
                    return

            if event_to_process.random_event_counter > 0:
                if random.random() > 0.25:
                    event_to_process.spread_step_count += 1
                event_to_process.random_event_counter -= 1
            else:
                event_to_process.spread_step_count -= 1

            # determine the directions to move towards
            directions = random.sample(
                ["up", "down", "left", "right"],
                random.randint(
                    *mapper.get_env_spread_direction_count(
                        key=event_to_process.enviornment_spawn_type
                    )
                ),
            )

            events_to_queue = []

            if event_to_process.position_x - 1 >= 0 and "up" in directions:
                # can move up
                events_to_queue.append({
                    "position_x": event_to_process.position_x - 1,
                    "position_y":event_to_process.position_y
                })


            if event_to_process.position_x + 1 < self.settings.tiles_along_x and "down" in directions:
                # can move_down
                events_to_queue.append({
                    "position_x": event_to_process.position_x + 1,
                    "position_y":event_to_process.position_y
                })

            if event_to_process.position_y - 1 >= 0 and "left" in directions:
                # can move left
                events_to_queue.append({
                    "position_x": event_to_process.position_x,
                    "position_y":event_to_process.position_y - 1
                })

            if event_to_process.position_y + 1 < self.settings.tiles_along_y and "right" in directions:
                # can move left
                events_to_queue.append({
                    "position_x": event_to_process.position_x,
                    "position_y":event_to_process.position_y + 1
                })

            for event in events_to_queue:
                tile_identifier = (event["position_x"],event["position_y"])
                if tile_identifier in self.tile_with_event_tracker:
                    continue

                self.tile_with_event_tracker.add(tile_identifier)
                self.env_tick_queue.append(EnviornmentTick(
                    position_x=event["position_x"],
                    position_y=event["position_y"],
                    tick_type=EnvTickType.passive,
                    random_event_counter=event_to_process.random_event_counter,
                    spread_step_count=event_to_process.spread_step_count,
                    enviornment_spawn_type=event_to_process.enviornment_spawn_type,
                    enviornment_attribute=event_to_process.enviornment_attribute
                ))

    def process_loop(self):
        """
        This function is responsible for creating and processing enviornmental events
        """

        # generate new enviornmental event if needed
        if len(self.env_tick_queue) < self.settings.env_tick_process_rate:
            for y_cord in random.sample(
                range(self.settings.tiles_along_y), self.settings.env_tick_generate_rate
            ):
                x_cord = random.randint(0, self.settings.tiles_along_x - 1)

                tile_identifier = (x_cord, y_cord)

                if tile_identifier in self.tile_with_event_tracker:
                    continue

                self.tile_with_event_tracker.add(tile_identifier)
                self.env_tick_queue.append(
                    EnviornmentTick(
                        position_x=x_cord,
                        position_y=y_cord,
                        random_event_counter=random.randint(0, 10),
                    )
                )


        # process existing enviornmental events
        counter = 0
        while (
            counter < self.settings.env_tick_process_rate
            and len(self.env_tick_queue) > 0
        ):

            self.process_env_tick()

            counter += 1
