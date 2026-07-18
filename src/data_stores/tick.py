from src.utils.enums import (
    BaseEnviornmentTypes, 
    EntityTypes, 
    EnviornmentalAttributes,
    EnvTickType
)


class EnviornmentTick:
    # stores the details about an enviornment tick
    def __init__(
        self,
        position_x: int,
        position_y: int,
        random_event_counter: int,
        tick_type: EnvTickType = EnvTickType.active,
        spread_step_count: int | None = None,
        enviornment_spawn_type: BaseEnviornmentTypes | None = None,
        enviornment_attribute: EnviornmentalAttributes | None = None,
    ):
        self.position_x: int = position_x
        self.position_y: int = position_y
        self.tick_type: EnvTickType = tick_type
        self.random_event_counter: int = random_event_counter
        self.spread_step_count: int = spread_step_count
        self.enviornment_spawn_type: BaseEnviornmentTypes | None = (
            enviornment_spawn_type
        )
        self.enviornment_attribute: EnviornmentalAttributes | None = (
            enviornment_attribute
        )


class EntityTick:
    # stores the details about an entity tick
    def __init__(
        self,
        x_cord: int,
        y_cord: int,
        pack_size: int | None = None,
        spawn_type: None | EntityTypes = None,
    ):
        self.x_cord: int = x_cord
        self.y_cord: int = y_cord
        self.pack_size: int = pack_size
        self.spawn_type: None | EntityTypes = spawn_type
