"""
This class is responsible for holding the global configs or settings.
That way i wont need to pass things around as much
"""


class GlobalSettings:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        scale_along_x: int,
        scale_along_y: int,
    ):
        if self._initialized:
            return

        # these will determine the size of the world
        # these will also be used to calculate the coordinate system for entities
        self.tiles_along_x: int = 390
        self.tiles_along_y: int = 246
        self.scale_along_x: int = scale_along_x
        self.scale_along_y: int = scale_along_y

        self.offset_from_window_edge: int = 10
        self.area_border_offset: int = 5

        # now we will store the details about the area above the game area
        self.tracker_area_x_length: int = self.tiles_along_x * self.scale_along_x
        self.tracker_area_y_length: int = 80  # keep this static for now

        self.tracker_area_x_offset: int = (
            self.offset_from_window_edge + self.area_border_offset
        )

        self.tracker_area_y_offset: int = (
            self.offset_from_window_edge + self.area_border_offset
        )

        # now we will store the detail about the game area
        self.game_area_x_length: int = self.tiles_along_x * self.scale_along_x
        self.game_area_y_length: int = self.tiles_along_y * self.scale_along_y

        self.game_area_x_offset: int = (
            self.offset_from_window_edge + self.area_border_offset
        )

        self.game_area_y_offset: int = (
            self.tracker_area_y_length
            + (2 * self.offset_from_window_edge)
            + (3 * self.area_border_offset)
        )

        # now we will calculat the size of the window
        self.window_length: int = (
            (self.tiles_along_x * self.scale_along_x)
            + (2 * self.offset_from_window_edge)
            + (2 * self.area_border_offset)
        )
        self.window_height: int = (
            self.tracker_area_y_length
            + self.game_area_y_length
            + (3 * self.offset_from_window_edge)
            + (4 * self.area_border_offset)
        )

        # game process rate
        self._fps: int = 60
        self.env_tick_generate_rate: int = 5
        self.env_tick_process_rate: int = 100


        self._initialized = True

    @property
    def frames_per_second(self):
        return self._fps

    @frames_per_second.setter
    def frames_per_second(self, value: int):
        if type(value) != int:
            raise Exception(f"Frame rate cannot be non integer value - {value}")
        self._fps = value

    @property
    def board_size_enviornment(self):
        return self.tiles_along_x * self.tiles_along_x
