from src.enviornment.base_env import EnviornmentBase
from src.utils.enums import EnviornmentalAttributes, TopEnviornmentTypes, EnvTickType

class WaterEnviornment(EnviornmentBase):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(64, 164, 223), 
            hunger_restore=0, 
            thirst_restore=5,
            top_layers={
                EnviornmentalAttributes.fertility: {
                    EnvTickType.active: [TopEnviornmentTypes.marsh],
                }
            }
        )