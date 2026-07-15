from enum import Enum

class EnviornmentTypes(Enum):
    grass = "grass"
    water = "water"
    tree = "tree"
    carrot = "carrot"
    rock = "rock"

class ElementType(Enum):
    enviornment = "Enviornment"
    entity = "Entity"

class EntityTypes(Enum):
    rabbit = "rabbit"

class EntityFoodType(Enum):
    carnivore = "carnivore"
    herbivore = "herbivore"
    omnivore = "omnivore"

class Direction(Enum):
    up = "up"
    down = "down"
    left = "left"
    right = "right"

class EntityActions(Enum):
    wander = "wander"
    eat = "eat"
    drink = "drink"
    idle = "idle"
    escape = "escape"
    chase = "chase"
    turn = "turn"