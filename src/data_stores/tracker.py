# this class will track each individual element

from src.entity.base import BaseEntity
from src.utils.enums import ElementType
from src.enviornment.base_env import EnviornmentBase

class Tracker:
    def __init__(
        self,
        element_type: ElementType,
        weight: float,
    ):
        # supplied variables
        self.element_type: ElementType = element_type
        self.weight: float = weight

        # tracking variables
        self._current_count: int = 0

    @property
    def current_count(self):
        return self._current_count
    
    @current_count.setter
    def current_count(self,value: int):
        self._current_count += value

    