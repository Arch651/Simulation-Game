import pygame
from rich import print

from src.manager.enviornment_world import EnviornmentWorldManager
from src.manager.settings import GlobalSettings


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
        
        self.settings: GlobalSettings = GlobalSettings(
            scale_along_x=length_per_pixel,
            scale_along_y=width_per_pixel
        )

        # we need to store the game window object as it needs to be 
        # passed to every tile for rendering
        self.window = pygame.display.set_mode(
            (self.settings.window_length, self.settings.window_height),
        )

        pygame.display.set_caption("Simulation game")
        self.game_clock = pygame.time.Clock()

        self.running: bool = True
        self.world_manager: EnviornmentWorldManager = EnviornmentWorldManager(
            window=self.window,
            settings=self.settings
        )

    def generate_base_game_view(self,only_game_area:bool = False) -> None:
        # this function will redraw the base layer of the game display for when 
        # the game starts or gets restarted or resized

        if not only_game_area:
            self.window.fill((0, 0, 0))

            pygame.draw.rect(
                surface=self.window,
                color=(193, 154, 107),
                rect=pygame.Rect(
                    (self.settings.offset_from_window_edge + self.settings.area_border_offset),
                    (self.settings.offset_from_window_edge + self.settings.area_border_offset),
                    self.settings.tracker_area_x_length,
                    self.settings.tracker_area_y_length
                ),
            )

            pygame.draw.rect(
                surface=self.window,
                color=(101, 67, 33),
                rect=pygame.Rect(
                    self.settings.offset_from_window_edge,
                    self.settings.offset_from_window_edge,
                    (self.settings.tracker_area_x_length + (2 * self.settings.area_border_offset)),
                    (self.settings.tracker_area_y_length + (2 * self.settings.area_border_offset))
                ),
                width=self.settings.area_border_offset,
                border_radius=5
            )

        #create the border around the game area
        pygame.draw.rect(
            surface=self.window,
            color=(101, 67, 33),
            rect=pygame.Rect(
                self.settings.offset_from_window_edge,
                (self.settings.game_area_y_offset - self.settings.area_border_offset),
                (self.settings.game_area_x_length + (2 * self.settings.area_border_offset)),
                (self.settings.game_area_y_length + (2 * self.settings.area_border_offset))
            ),
            width=self.settings.area_border_offset,
            border_radius=5
        )      

    
    def main_game_loop(self):
        """
        The main game loop that controls when each function gets called and controls the main game 
        """
        # Operations that need to be performed before the game starts
        self.generate_base_game_view()
        self.world_manager.generate_game_world()

        while self.running:
            # check if the game window has been closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #=============================================================#
            # the main game function wil go here
            self.world_manager.render_tile()
            self.world_manager.process_loop()
            
            #=============================================================#
            # final block that displays the frame on the screen
            pygame.display.flip()
            self.game_clock.tick(self.settings.frames_per_second)

            