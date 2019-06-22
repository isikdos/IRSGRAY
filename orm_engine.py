from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

"""
Create the engine that connects to the database
This establishes a database connection
and is the backbone of the ORM.
"""
def Create_Engine(connection_string):
    return create_engine(connection_string, echo=False)

"""
Configures itself with an engine, and then can be used
to generate identically configured sessions.
"""
def Create_Master_Session(engine):
    master_session = sessionmaker(bind = engine)
    return master_session
 
"""
Creates an automatically and perfectly configured session
such that abstracted pythonic operations can begin to be 
performed on it without overly minding what's going on in
the database's world.
"""
def Create_Session(master_session):
    session = master_session()
    return session

"""
An individual object that can take care of all the
database connectivity and session distribution
all by itself. Now elsewhere there just needs
tobe an instantiation of the sessionfactory
and it can be blind to everything else.
"""
class SessionFactory():
    def __init__(self, connection_string):
        logger = logging.getLogger(__name__)

        try:
            self.engine = Create_Engine(connection_string)
        except BaseException as e:
            logger.exception("Unknown error creating the engine with connection string {0}. EXCEPTION:\n{1}".format(connection_string, e))
            raise e
       
        try:
            self.master_session = Create_Master_Session(self.engine)
        except BaseException as e:
            logger.exception("Unknown error creating the master session based on connection string {0}. EXCEPTION:\n{1}".format(connection_string, e))
            raise e    

    def Create_Session(self):
        session = Create_Session(self.master_session)
        return session
