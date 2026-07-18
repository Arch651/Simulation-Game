from src.utils.enums import (
    EntityTypes,
    TopEnviornmentTypes,
    BaseEnviornmentTypes,
    EnviornmentalAttributes,
)

from src.entity.rabbit import RabbitEntity
from src.enviornment.base import (
    GrassEnviornment,
    WaterEnviornment,
    MountainEnviornment,
    BarrenEnviornment
)
from src.enviornment.top import (
    CropEnviornment,
    TreeEnviornment,
    SandEnviornment,
    SnowEnviornment,
    MudEnviornment,
    MarshEnviornment,
)


class Mapper:

    _env_attribute_to_base_env_map = {
        EnviornmentalAttributes.fertility: [BaseEnviornmentTypes.grass],
        EnviornmentalAttributes.hydration: [BaseEnviornmentTypes.water],
        EnviornmentalAttributes.hardness: [BaseEnviornmentTypes.mountain]
    }

    _env_to_weight_map = {
        BaseEnviornmentTypes.grass : 0.3,
        BaseEnviornmentTypes.water: 0.2,
        BaseEnviornmentTypes.mountain: 0.05,
        BaseEnviornmentTypes.barren: 0.05,

        TopEnviornmentTypes.crop: 0.15,
        TopEnviornmentTypes.tree: 0.1,
        TopEnviornmentTypes.marsh: 0.2,
        TopEnviornmentTypes.mud: 0.3,
        TopEnviornmentTypes.sand: 0.3,
        TopEnviornmentTypes.snow: 0.5,
    }

    _env_to_class_map = {
        BaseEnviornmentTypes.grass : GrassEnviornment,
        BaseEnviornmentTypes.water: WaterEnviornment,
        BaseEnviornmentTypes.mountain: MountainEnviornment,
        BaseEnviornmentTypes.barren: BarrenEnviornment,

        TopEnviornmentTypes.marsh: MarshEnviornment,
        TopEnviornmentTypes.mud: MudEnviornment,
        TopEnviornmentTypes.sand: SandEnviornment,
        TopEnviornmentTypes.snow: SnowEnviornment,
        TopEnviornmentTypes.crop: CropEnviornment,
        TopEnviornmentTypes.tree: TreeEnviornment

    }

    _env_to_size_map = {
        BaseEnviornmentTypes.grass : (3,40),
        BaseEnviornmentTypes.water: (10,20),
        BaseEnviornmentTypes.mountain: (15,25),
        BaseEnviornmentTypes.barren: (10,20),

        TopEnviornmentTypes.marsh: (1,5),
        TopEnviornmentTypes.mud: (1,3),
        TopEnviornmentTypes.sand: (1,5),
        TopEnviornmentTypes.snow: (1,5),
        TopEnviornmentTypes.crop: (1,5),
        TopEnviornmentTypes.tree: (1,5),
    }

    _env_to_spread_direction_count_map = {
        BaseEnviornmentTypes.grass : (1,4),
        BaseEnviornmentTypes.water: (1,4),
        BaseEnviornmentTypes.mountain: (3,4),
        BaseEnviornmentTypes.barren: (1,3),

        TopEnviornmentTypes.marsh: (1,3),
        TopEnviornmentTypes.mud: (1,3),
        TopEnviornmentTypes.sand: (1,3),
        TopEnviornmentTypes.snow: (1,3),
        TopEnviornmentTypes.crop: (1,3),
        TopEnviornmentTypes.tree: (1,3),
    }

    _entity_to_pack_size_map = {
        EntityTypes.rabbit: (5,10), 
    }

    _entity_to_class_map = {
        EntityTypes.rabbit: RabbitEntity
    }

    _entity_to_weight_map = {
        EntityTypes.rabbit: 0.005
    }

    
    def get_base_env_for_env_attributes(self, key: EnviornmentalAttributes):
        return self._env_attribute_to_base_env_map[key]

    def get_env_weight(self,key: BaseEnviornmentTypes):
        return self._env_to_weight_map[key]
    
    def get_entity_weight(self,key: EntityTypes):
        return self._entity_to_weight_map[key]
    
    def get_env_class(self,key: BaseEnviornmentTypes):
        return self._env_to_class_map[key]
    
    def get_env_size(self,key: BaseEnviornmentTypes):
        return self._env_to_size_map[key]
    
    def get_entity_pack_size(self,key: EntityTypes):
        return self._entity_to_pack_size_map[key]
    
    def get_entity_class(self,key: EntityTypes):
        return self._entity_to_class_map[key]
    
    def get_env_spread_direction_count(self,key: BaseEnviornmentTypes):
        return self._env_to_spread_direction_count_map[key]


mapper = Mapper()