import pygame
from rich import print

from src.manager.world import WorldManager
from src.manager.action import EntityAction
from src.manager.entity import EntityTracker
from src.manager.enviornment import EnviornmentTracker
from src.entity.entity_generator import EntityGenerator
from src.enviornment.env_generator import EnviornmentGenerator

class GameManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self, 
        length_per_pixel: int,
        width_per_pixel: int,
    ):
        if self._initialized:
            return 
        
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
        self.game_refresh_tick_rate: int = 30
        self.action_loop_max_counter: int = 3 # experimental
        self.action_loop_current_counter: int = 0 # experimental

        # spawn factor information
        self.spawn_rate: int = 50
        self.queue_process_rate: int = 200
        self.last_refresh = None

        # now we store the different data stores. Things that will track the data for the game
        self.field_size: int  = self.game_world_x_pixels * self.game_world_y_pixels
        self.world_manager: None |  WorldManager = None
        
        self.env_generator: None | EnviornmentGenerator = None
        self.env_tracker: EnviornmentTracker = EnviornmentTracker(
            window=self.window,
            board_size=self.field_size
        )

        self.entity_generator: None | EntityGenerator = None
        self.entity_action_manager: None | EntityAction = None
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

    
    def main_game_loop(self):
        # parts of the game that should run before rendering like initial
        # enviornment and entity generation

        # generate the world object
        self.world_manager = WorldManager(
            window=self.window,
            game_world_x_pixels=self.game_world_x_pixels,
            game_world_y_pixels=self.game_world_y_pixels,
            length_per_pixel=self.length_per_pixel,
            width_per_pixel=self.width_per_pixel,
            entity_tracker=self.entity_tracker,
            env_tracker=self.env_tracker
        )

        # create the env generator
        if self.env_generator == None:
            self.env_generator = EnviornmentGenerator(
                spaces_on_x=self.game_world_x_pixels,
                spaces_on_y=self.game_world_y_pixels,
                world_manager=self.world_manager,
                new_event_gen_rate=self.spawn_rate,
                process_rate=self.queue_process_rate
            )

        # create entity generator
        if self.entity_generator == None:
            self.entity_generator = EntityGenerator(
                spaces_on_x=self.game_world_x_pixels,
                spaces_on_y=self.game_world_y_pixels,
                world_manager=self.world_manager,
                process_rate=self.queue_process_rate,
                new_entity_gen_rate=self.spawn_rate
            )

        self.entity_action_manager = EntityAction(
            entity_tracker=self.entity_tracker
        )

        # generate the game tiles
        self.world_manager.generate_game_world(
            game_x=self.game_x,
            game_y=self.game_y
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
                
                self.entity_action_manager.process_passive_actions()
                self.entity_tracker.remove_dead_entities()

                if self.action_loop_current_counter == self.action_loop_max_counter:
                    self.entity_action_manager.queue_voluntary_action() 
                    self.entity_action_manager.process_voluntary_actions()
                    self.action_loop_current_counter = 0
                else:
                    self.action_loop_current_counter += 1

                self.last_refresh = current_loop_start

            has_rendered = self.world_manager.render_tile()
            if has_rendered:
                self.generate_base_game_view(
                    only_game_area=True
                )

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
            