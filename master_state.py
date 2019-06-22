import orm_engine
import logging
import sys
import os
from orm_engine import SessionFactory

"""
Exists as a place to contain both the configuration arguments
and the highest level connection to the database.
Because it is related to the launch configuration and 
directly wired into the database, I call it the Master State

The MasterState also contains all the up-to-date runtime information
regarding Enumeration Values. These enumerations are initially taken from the 
file database_enumerations and then are compared against the database,
and finally replaced with the real database values.
"""
class MasterState():

    class Enumerations():
        BehaviorEnum = None
        TimePeriodEnum = None

    # This is where the cached in-memory
    # enums go
    enumerations = Enumerations()
    
    def __init__(self, config_args):
        self.args = config_args
        self.session_factory = SessionFactory(config_args.connection_string)

    def Set_Enumerations(self, behavior_enum, time_period_enum):
        self.enumerations.BehaviorEnum = behavior_enum
        self.enumerations.TimePeriodEnum = time_period_enum


