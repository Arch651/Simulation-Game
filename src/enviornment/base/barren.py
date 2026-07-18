from src.enviornment.base_env import EnviornmentBase
from src.utils.enums import EnviornmentalAttributes, TopEnviornmentTypes, EnvTickType

class BarrenEnviornment(EnviornmentBase):
    def __init__(self,window):
        super().__init__(
            window=window, 
            color=(139, 115, 85), 
            hunger_restore=0, 
            thirst_restore=0,
            top_layers={
                EnviornmentalAttributes.hardness: {
                    EnvTickType.active: [
                        TopEnviornmentTypes.sand
                    ],
                }
            }
        )