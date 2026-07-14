from src.utils.enums import EnviornmentTypes, EntityTypes


class EnviornmentTick:
    # stores the details about an enviornment tick
    def __init__(
        self,
        x_cord: int,
        y_cord: int,
        proc_randomness: int,
        growth_potential: int | None = None,
        spawn_type: None | EnviornmentTypes = None
    ):
        self.x_cord: int = x_cord
        self.y_cord: int = y_cord
        self.proc_randomness: int = proc_randomness
        self.growth_potential: int = growth_potential
        self.spawn_type: None | EnviornmentTypes = spawn_type

class EntityTick:
    # stores the details about an entity tick
    def __init__(
        self,
        x_cord: int,
        y_cord: int,
        pack_size: int | None = None,
        spawn_type: None | EntityTypes = None
    ):
        self.x_cord: int = x_cord
        self.y_cord: int = y_cord
        self.pack_size: int = pack_size
        self.spawn_type: None | EntityTypes = spawn_type
        
