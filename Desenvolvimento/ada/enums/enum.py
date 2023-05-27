from enum import Enum

class Period(Enum):
    morning = 'morning'
    afternoon = 'afternoon'
    night = 'night'

class Day(Enum):
    monday = 'monday'
    tuesday = 'tuesday'
    wednesday = 'wednesday'
    thursday = 'thursday'
    friday = 'friday'
    saturday = 'saturday'

class Priority(Enum):
    primary = 'primary'
    secondary = 'secondary'