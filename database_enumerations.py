import schema
from enum import Enum

"""
These objects live to die.

Initially spawning in with the actual data, their only job is to verify that an object with
this information exists within the database. After that is done, a transformed version of them
which is, instead of a symbolization of the objects, the LITERAL OBJECT, is placed inside of the
master state. These are discardable afterwards.

"""


class BehaviorEnum(Enum):
    Cooperative = {"model": schema.Behavior, "BehaviorName": "Cooperative", "BehaviorIsPositive": True}
    SelfCare = 	{"model": schema.Behavior, "BehaviorName": "Self Care", "BehaviorIsPositive": True} 
    Safe = {"model": schema.Behavior, "BehaviorName": "Safe", "BehaviorIsPositive": True}  
    PDI = {"model": schema.Behavior, "BehaviorName": "PDI", "BehaviorIsPositive": True}  
    PDII = {"model": schema.Behavior, "BehaviorName": "PDII", "BehaviorIsPositive": True}  
    EI = {"model": schema.Behavior, "BehaviorName": "EI", "BehaviorIsPositive": True}  
    EII = {"model": schema.Behavior, "BehaviorName": "EII", "BehaviorIsPositive": True}  
    VPThreats = {"model": schema.Behavior, "BehaviorName": "V/P Threats", "BehaviorIsPositive": False}  
    Aggression = {"model": schema.Behavior, "BehaviorName": "Aggression", "BehaviorIsPositive": False}  
    Opposition = {"model": schema.Behavior, "BehaviorName": "Opposition", "BehaviorIsPositive": False}  

class TimePeriodEnum(Enum):
    TimePeriod01 = {"model": schema.TimePeriod, "TimePeriodStartTime": 27900, "TimePeriodEndTime": 28380}
    TimePeriod02 = {"model": schema.TimePeriod, "TimePeriodStartTime": 28380, "TimePeriodEndTime": 31500}
    TimePeriod03 = {"model": schema.TimePeriod, "TimePeriodStartTime": 31500, "TimePeriodEndTime": 34620}
    TimePeriod04 = {"model": schema.TimePeriod, "TimePeriodStartTime": 34620, "TimePeriodEndTime": 35040}
    TimePeriod05 = {"model": schema.TimePeriod, "TimePeriodStartTime": 35040, "TimePeriodEndTime": 38160}
    TimePeriod06 = {"model": schema.TimePeriod, "TimePeriodStartTime": 38160, "TimePeriodEndTime": 39480}
    TimePeriod07 = {"model": schema.TimePeriod, "TimePeriodStartTime": 39480, "TimePeriodEndTime": 42600}
    TimePeriod08 = {"model": schema.TimePeriod, "TimePeriodStartTime": 39000, "TimePeriodEndTime": 45000}
    TimePeriod09 = {"model": schema.TimePeriod, "TimePeriodStartTime": 45000, "TimePeriodEndTime": 48120}
    TimePeriod10 = {"model": schema.TimePeriod, "TimePeriodStartTime": 48120, "TimePeriodEndTime": 51300}

