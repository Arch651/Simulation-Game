# This will store the world class
# This class is responsible for storing the information about the world
# every cell in the world will be a tile. These individual units will be responsible for keeping 
# track about themselves. They will also be responsible for rendering and interactions
# This class will only store the overall data points like a wrapper. Any thing that is shared
# with other objects will be stored here
# This class is responsible for controlling the flow of events and passing data around
import math
import pygame
from rich import print

from src.data_stores.tile import Tile
from src.manager.entity import EntityTracker
from src.manager.enviornment import EnviornmentTracker
from src.entity.entity_generator import EntityGenerator
from src.enviornment.env_generator import EnviornmentGenerator

class World:
    def __init__(
        self, 
        length_per_pixel: int,
        width_per_pixel: int,
    ):
        # fixed values
        self.offset: int = 10
        self.title_width: int = 80
        self.game_world_x_pixels: int = 195 # 390 
        self.game_world_y_pixels: int = 123 # 246 

        # store the dimension of the game window these are used for all the rendering
        self.length_per_pixel: int = length_per_pixel
        self.width_per_pixel: int = width_per_pixel
        self.window_length: int = (
            self.game_world_x_pixels * self.length_per_pixel + (2 * self.offset)
        )

        self.window_width: int = (
            self.game_world_y_pixels * self.width_per_pixel 
            + (3 * self.offset)
            + self.title_width
        )

        # now we need to calculate the space that needs to be left at the top
        self.should_redraw: bool = True
        self.title_x: int = self.offset
        self.title_y: int = self.offset
        

        self.game_x: int = self.offset
        self.game_y: int = (2 * self.offset) + self.title_width

        # we need to store the game window object as it needs to be 
        # passed to every tile for rendering
        self.window = pygame.display.set_mode(
            (self.window_length, self.window_width),
        )

        pygame.display.set_caption("Simulation game")
        self.game_clock = pygame.time.Clock()

        self.running: bool = True
        self._tick_rate: int = 60 # default will be 60
        self.game_refresh_tick_rate: int = 10

        # spawn factor information
        self.spawn_rate: int = 50
        self.queue_process_rate: int = 200
        self.last_refresh = None

        # entity factor information

        # now we store the different data stores. Things that will track the data for the game
        self.field_size: int  = self.game_world_x_pixels * self.game_world_y_pixels

        self.tile_grid: list[list[Tile]] = []
        
        self.env_generator: None | EnviornmentGenerator = None
        self.env_tracker: EnviornmentTracker = EnviornmentTracker(
            window=self.window,
            board_size=self.field_size
        )

        self.entity_generator: None | EntityGenerator = None
        self.entity_tracker: EntityTracker = EntityTracker(
            window=self.window,
            board_size=self.field_size
        )


    def generate_base_game_view(self,only_game_area:bool = False):
        # this function will redraw the base layer of the game display for when 
        # the game starts or gets restarted or resized

        if not only_game_area:
            self.window.fill((0, 0, 0))

            # create the area with the stats and menus
            # this area will always consume 100 pixles
            title_rect_object = pygame.Rect(
                self.title_x - 2,
                self.title_y,
                (self.game_world_x_pixels * self.length_per_pixel) + 4,
                self.title_width
            )

            pygame.draw.rect(
                surface=self.window,
                color=(193, 154, 107),
                rect=title_rect_object,
                border_radius=5
            )

            pygame.draw.rect(
                surface=self.window,
                color=(101, 67, 33),
                rect=title_rect_object,
                width=5,
                border_radius=5
            )

        # now lets draw the game render area
        game_rect_object = pygame.Rect(
            self.game_x - 2,
            self.game_y - 2,
            (self.game_world_x_pixels * self.length_per_pixel) + 4,
            (self.game_world_y_pixels * self.width_per_pixel) + 4
        ) # offset it by 2 pixels each to make the border render around the actual data

        pygame.draw.rect(
            surface=self.window,
            color=(101, 67, 33),
            rect=game_rect_object,
            width=5,
            border_radius=5
        )

    
    def generate_game_world(self):
        # generate the tiles that will handle the game logic at a pixel
        for y_cord in range(self.game_world_y_pixels):
            res = []
            for x_cord in range(self.game_world_x_pixels):
                res.append(Tile(
                    x_cord=math.ceil(x_cord * self.length_per_pixel) + self.game_x,
                    y_cord=math.ceil(y_cord * self.width_per_pixel) + self.game_y,
                    length=self.length_per_pixel,
                    width=self.width_per_pixel, 
                    window=self.window,
                    board_size=self.field_size
                ))
            self.tile_grid.append(res)
    
    def render_tile(self):
        has_updated = False

        for row in self.tile_grid:
            for tile in row:
                if tile.has_updated:
                    tile.render()
                    has_updated = True
        
        if has_updated:
            self.generate_base_game_view(
                only_game_area = True
            )        

    
    def main_game_loop(self):

        # parts of the game that should run before rendering like initial
        # enviornment and entity generation

        self.generate_game_world()

        # create the env generator
        if self.env_generator == None:
            self.env_generator = EnviornmentGenerator(
                spaces_on_x=self.game_world_x_pixels,
                spaces_on_y=self.game_world_y_pixels,
                tile_grid=self.tile_grid,
                new_event_gen_rate=self.spawn_rate,
                process_rate=self.queue_process_rate
            )

        # create entity generator
        if self.entity_generator == None:
            self.entity_generator = EntityGenerator(
                spaces_on_x=self.game_world_x_pixels,
                spaces_on_y=self.game_world_y_pixels,
                tile_grid=self.tile_grid,
                process_rate=self.queue_process_rate,
                new_entity_gen_rate=1 #self.spawn_rate
            )

        while self.running:
            # check if the game window has been closed

            current_loop_start = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # main game logic
            if self.should_redraw:
                self.generate_base_game_view()
                self.should_redraw = False

            if (
                self.last_refresh == None 
                or current_loop_start - self.last_refresh > self.game_refresh_tick_rate
            ):
                # after a set amount of time we will try to update the env again
                self.env_generator.process_loop()
                self.entity_generator.process_loop()
                self.last_refresh = current_loop_start

            self.render_tile()

            # final block that displays the frame on the screen
            pygame.display.flip()
            self.game_clock.tick(self.tick_rate)


    @property
    def tick_rate(self):
        return self._tick_rate
    
    @tick_rate.setter
    def tick_rate(self,value: int):
        if self.tick_rate < 1:
            # we will keep it at the current rate
            pass
        else:
            self.tick_rate = value