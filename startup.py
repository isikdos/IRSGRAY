from configparser import ConfigParser
import os
import sys
import logging
import logging.config
from master_state import MasterState
from shared import Get_One_Or_Create
from database_enumerations import TimePeriodEnum, BehaviorEnum
import schema
from enum import Enum

"""
Performs all onetime configuration initialization
and creates all objects that need to be spawned
before anything else can really happen.
"""
def startup(CONFIG = None, SERVICE = None):
    # Pull initialization data from environment varialbles
    config_file = CONFIG or os.getenv("CONFIG")
    profile_name = SERVICE or os.getenv("SERVICE")

    # Validate that they're potentially useful
    Validate_Environment_Variables(config_file, profile_name)

    # Use the environment variables to begin pulling data from a config file
    config_args = Get_Startup_Config_Args(config_file, profile_name)
    
    # Verify that the config arguments are well structured
    Validate_Config_Arguments(config_file, profile_name, config_args)

    #NOTE:
    # Performs global logging configuration
    # Even though nothing is returned,
    # _EVERYTHING HAS CHANGED_
    Initialize_Logging(config_args.logging_config)

    # Now we can stop doing sys.stderr.write
    # and begin making calls to the logger
    logger = logging.getLogger(__name__)

    ms = MasterState(config_args)

    # These are NEW ENUMERATION OBJECTS
    # that reflect the OBJECT IN THE DATABASE
    # instead of a set of attributes
    behavior_enum, time_period_enum = Initialize_Database(ms)

    ms.Set_Enumerations(behavior_enum, time_period_enum)

    return ms
    

"""
Disassemble all old logging handlers
And implement the ones defined in the
file being queried.
"""
def Initialize_Logging(logging_config):

    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)
    logging.config.fileConfig(logging_config, disable_existing_loggers=False)

"""
Validate the arguments that we are pulling from the main configuration file in 
the selected profile. Test that they are part of the namespace, then test
that they have potentially valid values.

Args:
    config_file: string
      - The config file, at this point more or less guaranteed to be correct
    profile_name: string
      - The section of the config file, at this point more or less guaranteed to be correct
    config_args: GenericNamespace
      - Contains the values that we are now attempting to validate.

Return:
    None

Notes: 
    On failure, emits an error message and then exits.
    
"""
def Validate_Config_Arguments(config_file, profile_name, config_args):
    try:
        logging_conf = config_args.logging_config
    except AttributeError:
        sys.stderr.write("The main configuration file {0} in section {1} does not have the field 'logging-config' defined. Quitting.\n".format(config_file, profile_name))
        sys.exit()
    else:
        if not logging_conf:
            sys.stderr.write("The logging config in main configuration file {0} in section {1} is not well defined.\n".format(config_file, profile_name))
            sys.exit()
        if not os.path.isfile(logging_conf):
            sys.stderr.write("The logging config file {0} in main configuration file {1} in section {2} is not actually a file.\n".format(logging_conf, config_file, profile_name))
            sys.exit()

    try:
        connection_string = config_args.connection_string
    except AttributeError:
        sys.stderr.write("The main configuration file {0} in section {1} does not have the field 'connection-string' defined. Quitting.\n".format(config_file, profile_name))
        sys.exit()
    else:
        if not connection_string:
            sys.stderr.write("The connection string in main configuration file {0} in section {1} is not well defined.\n".format(config_file, profile_name))
            sys.exit()

    return

"""
Validate the hypothetical utility of the 
required environment variables. Doesn't actually
use them but instead checks for their existence
and makes sure they seem sane, or represent
what they are supposed to.

args:
    config_file: string
       - Derived from environment variable CONFIG. Points to the
         main configuration file where all the initialization takes place.
    profile_name: string
       - Derived from environment variable SERVICE. Points to the
         section in the main configuration file where the arguments are.

    Return: 
        None

    Notes:
        If validation fails, an error message will be emitted and then the
        program will exit immediately.
"""
def Validate_Environment_Variables(config_file, profile_name):
    if config_file is None:
        sys.stderr.write("Environment variable CONFIG is not defined. Please define environment variable CONFIG and point it towards the main configuration file\n")
        sys.exit()
    if profile_name is None:
        sys.stderr.write("Environment variable SERVICE is not defined. Please define environment variable SERVICE and make it the name of the section in the main configuration file\n")
        sys.exit()

    if not os.path.isfile(config_file):
        sys.stderr.write("Defined environment variable CONFIG evaluates to <{0}> which is not a file.\n".format(config_file))
        sys.exit()

    return

"""
Load config values from the main.conf file defined in
the CONFIG environment variable. Pulls the values out
of the configuration file and returns them in an all-
purpose namespace object that can have validation 
performed against it.

Args:
    config_file:
       - Derived from environment variable CONFIG. Points to the
         main configuration file where all the initialization takes place.
    profile_name: string
       - Derived from environment variable SERVICE. Points to the
         section in the main configuration file where the arguments are.

Return:
    args: GenericNamespace
       - A namespace object with an attribute for every field in 
         the config section.
"""
def Get_Startup_Config_Args(config_file, profile_name):

    cp = ConfigParser()
    try:
        cp.read(config_file)
    except BaseException as e:
        sys.stderr.write("Unknown exception reading profile name {0} from config file {1}. EXCEPTION:\n{2}\n".format(profile_name, config_file, e))
        raise e

    try:
        args_dt = cp[profile_name]
    except KeyError as e:
        sys.stderr.write("Config file {0} has no section defined by the environment variable SERVICE = {1}. The header of the config file should be expressed as (with brackets) [{1}]\n".format(config_file, profile_name))
        raise e

    args = GenericNamespace(args_dt)

    return args    


"""
For creating any object you want! 
"""
class GenericNamespace():
    def __init__(self, adict):
        new_dict = dict()
        for i in adict:
            new_i = i.replace("-","_")
            new_dict[new_i] = adict[i]  

        self.__dict__.update(new_dict)


def Initialize_Database(masterstate):
    logger = logging.getLogger(__name__)

    session = masterstate.session_factory.Create_Session()

    # Now we're going to create new instances of these enumerations
    # instead of weak facsimiles, they're going to BE the database
    # objects

    # Literally if you don't understand what's going on here 
    # then please don't fuck with it
    # cheers!

    new_enum_dt = dict()
    for i in BehaviorEnum:
        behavior, exists = Get_One_Or_Create(session, **i.value)
        new_enum_dt[i.name] = behavior
    new_behavior_enum = Enum('BehaviorEnum', new_enum_dt)

    new_enum_dt = dict()
    for i in TimePeriodEnum:
        timeperiod, exists = Get_One_Or_Create(session, **i.value)
        new_enum_dt[i.name] = timeperiod
    new_timeperiod_enum = Enum('TimePeriodEnum', new_enum_dt)

    try:
        session.commit() 
    except BaseException as e:
        logger.exception("Error committing database initialization. Failed to initialize the database properly... cannot continue. EXITING. EXCEPTION:\n{0}".format(e))
        sys.exit() 

    session.close()
    return new_behavior_enum, new_timeperiod_enum
