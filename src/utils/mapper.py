from src.utils.enums import (
    EntityTypes,
    EnviornmentTypes,
)

from src.entity.rabbit import RabbitEntity
from src.enviornment.tree import TreeEnviornment
from src.enviornment.rock import RockEnviornment
from src.enviornment.grass import GrassEnviornment
from src.enviornment.water import WaterEnviornment
from src.enviornment.carrot import CarrotEnviornment


class Mapper:
    _env_to_weight_map = {
        EnviornmentTypes.grass : 0.3,
        EnviornmentTypes.water: 0.2,
        EnviornmentTypes.tree: 0.05,
        EnviornmentTypes.carrot: 0.1,
        EnviornmentTypes.rock: 0.05
    }

    _env_to_class_map = {
        EnviornmentTypes.grass : GrassEnviornment,
        EnviornmentTypes.water: WaterEnviornment,
        EnviornmentTypes.tree: TreeEnviornment,
        EnviornmentTypes.carrot: CarrotEnviornment,
        EnviornmentTypes.rock: RockEnviornment,
    }

    _env_to_size_map = {
        EnviornmentTypes.grass : (3,40),
        EnviornmentTypes.water: (10,20),
        EnviornmentTypes.tree: (10,15),
        EnviornmentTypes.carrot: (10,20),
        EnviornmentTypes.rock: (10,15),
    }

    _env_to_spread_direction_count_map = {
        EnviornmentTypes.grass : (1,4),
        EnviornmentTypes.water: (1,2),
        EnviornmentTypes.tree: (0,4),
        EnviornmentTypes.carrot: (0,4),
        EnviornmentTypes.rock: (0,3),
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

    

    def get_env_weight(self,key: EnviornmentTypes):
        return self._env_to_weight_map[key]
    
    def get_entity_weight(self,key: EntityTypes):
        return self._entity_to_weight_map[key]
    
    def get_env_class(self,key: EnviornmentTypes):
        return self._env_to_class_map[key]
    
    def get_env_size(self,key: EnviornmentTypes):
        return self._env_to_size_map[key]
    
    def get_entity_pack_size(self,key: EntityTypes):
        return self._entity_to_pack_size_map[key]
    
    def get_entity_class(self,key: EntityTypes):
        return self._entity_to_class_map[key]
    
    def get_env_spread_direction_count(self,key: EnviornmentTypes):
        return self._env_to_spread_direction_count_map[key]


mapper = Mapper()