# This will store the world class
# This class is responsible for storing the information about the world
# every cell in the world will be a tile. These individual units will be responsible for keeping 
# track about themselves. They will also be responsible for rendering and interactions
# This class will only store the overall data points like a wrapper. Any thing that is shared
# with other objects will be stored here
# This class is responsible for controlling the flow of events and passing data around
import math

from src.data_stores.tile import Tile
from src.manager.entity import EntityTracker
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
        window,
        game_world_x_pixels: int,
        game_world_y_pixels: int,
        length_per_pixel: int,
        width_per_pixel: int,
        entity_tracker: EntityTracker,
        env_tracker: EnviornmentTracker
    ):
        if self._initialized:
            return
        
        self.window = window
        self.entity_tracker: EntityTracker = entity_tracker
        self.env_tracker: EnviornmentTracker = env_tracker
        self.game_world_x_pixels: int = game_world_x_pixels
        self.game_world_y_pixels: int = game_world_y_pixels
        self.length_per_pixel: int = length_per_pixel
        self.width_per_pixel: int = width_per_pixel

        self.tile_grid: list[list[Tile]] = []
    
    def generate_game_world(self, game_x: int, game_y: int):
        # generate the tiles that will handle the game logic at a pixel
        for y_cord in range(self.game_world_y_pixels):
            res = []
            for x_cord in range(self.game_world_x_pixels):
                res.append(Tile(
                    window=self.window,
                    identifier=(x_cord,y_cord),
                    world=self,  # i am as amazed as the person who is seeing this
                    x_cord=math.ceil(x_cord * self.length_per_pixel) + game_x,
                    y_cord=math.ceil(y_cord * self.width_per_pixel) + game_y,
                    length=self.length_per_pixel,
                    width=self.width_per_pixel, 
                    entity_tracker=self.entity_tracker,
                    env_tracker=self.env_tracker
                ))
            self.tile_grid.append(res)
    
    def render_tile(self) -> bool:
        has_updated = False

        for row in self.tile_grid:
            for tile in row:
                if tile.has_updated:
                    tile.render()
                    has_updated = True
        
        return has_updated
    
    def get_tile_information(self,x_cord: int, y_cord: int) -> Tile:
        return self.tile_grid[y_cord][x_cord]
    
    @property
    def max_length(self):
        return self.game_world_x_pixels 
    
    @property
    def max_width(self):
        return self.game_world_y_pixels 