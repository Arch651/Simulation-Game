from enum import Enum

class EnviornmentalAttributes(Enum):
    hydration = "hydration"
    fertility = "fertility"
    hardness = "hardness"

class BaseEnviornmentTypes(Enum):
    """These are the enviornments that are spawned as the base layer"""
    grass = "grass"
    water = "water"
    mountain = "rock"
    barren = "barren"

class TopEnviornmentTypes(Enum):
    """These are the enviornment types that can grow on top of the base layer"""
    tree = "tree"
    crop = "crop"
    snow = "snow"
    sand = "sand"
    marsh = "marsh"
    mud = "mud"

class EnvTickType(Enum):
    active = "active"
    passive = "passive"

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