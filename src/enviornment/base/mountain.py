from src.enviornment.base_env import EnviornmentBase
from src.utils.enums import EnviornmentalAttributes, TopEnviornmentTypes, EnvTickType

class MountainEnviornment(EnviornmentBase):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(128, 128, 128), 
            hunger_restore=0, 
            thirst_restore=0,
            top_layers={
                EnviornmentalAttributes.hydration: {
                    EnvTickType.active: [TopEnviornmentTypes.snow],
                }
            }
        )