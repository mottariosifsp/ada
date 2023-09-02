from enum import Enum

class Period(Enum):
    morning = 'MORNING'
    afternoon = 'AFTERNOON'
    night = 'NIGHT'

class Day(Enum):
    monday = 'MONDAY'
    tuesday = 'TUESDAY'
    wednesday = 'WEDNESDAY'
    thursday = 'THURSDAY'
    friday = 'FRIDAY'
    saturday = 'SATURDAY'

class Priority(Enum):
    primary = 'PRIMARY'
    secondary = 'SECONDARY'

class Job(Enum):
    twenty_hours = 'TWENTY_HOURS'
    forty_hours = 'FORTY_HOURS'
    rde = 'RDE'
    temporary = 'TEMPORARY'
    substitute = 'SUBSTITUTE'
