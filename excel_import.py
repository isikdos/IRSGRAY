from shared import Get_One_Or_Create, Date_2_Int, Int_2_Date
from sqlalchemy.orm.exc import NoResultFound
import schema
import logging
import os
import time
from openpyxl import load_workbook

"""
Handles all the responsibilities associated with the
generic beginnings of an excel import. It validates
that what is being imported is a real file,
it creates the session associated with the import,
and it informs whether or not the file has been imported before.

Arguments:
  master_state - Master State
    - Contains all the info, has all the toys. 
  excel_file - string
    - Referent to a system file path that ends in a valid excel
      file.

Return:
  session - sql alchemy session
    - An atomic session to communicate with the sqllite database
  imported_file - sql alchemy ImportedFile
    - A representative object symbolizing the file specified
  isnew - boolean
    - Whether or not the imported_file already existed in the
      database, or if we're inserting it now.
"""
def Initialize_Excel_Import(master_state, excel_file):
    logger = logging.getLogger(__name__)
    
    if not os.path.isfile(excel_file):
        logger.error("Provided file name {0} is not referent to an actual file. Cannot import.")
        return

    excel_filename = os.path.basename(excel_file)

    session = master_state.session_factory.Create_Session()

    imported_file, isnew = Get_One_Or_Create(session, schema.ImportedFile, ImportedFileFullPath = excel_file, ImportedFileFileName = excel_filename)    

    return session, imported_file, isnew

"""
For importing an IRS file, from file format 01.
This is extremely specific to file format01. Not only
is it not guaranteed to work on any other formatted file,
it's basically guaranteed to NOT work on them. DON'T DO IT!
"""
def Import_IRS_01(master_state, excel_file):
    logger = logging.getLogger(__name__)

    # initialization...
    session, imported_file, isnew = Initialize_Excel_Import(master_state, excel_file)

    # In this case, we are NOT going to allow modifications.
    # TODO this should eventually be generically handled by some 
    # set of options in the vicinity of 'IsUpdatable' or somesuch
    # In the meantime and possibly forever, it can be handled at 
    # the start of files.
    if not isnew:
        _datetime = Int_2_Date(imported_file.ImportedFileInsertTime)
        logger.error("File {0} was already imported at time {1}, and this type of file cannot be imported multiple times. Will not import".format(excel_file, _datetime))
        session.rollback()
        session.close()
        return

    time_period_enum = master_state.enumerations.TimePeriodEnum
    behavior_enum = master_state.enumerations.BehaviorEnum 

    # These indices are used to
    # scroll over the to-be-imported excel document
    # a mapping of column and row will provide the 
    # information regarding a behavior/timeperiod
    col2behavior = {
        'B': behavior_enum.Cooperative.value,
        'C': behavior_enum.SelfCare.value,
        'D': behavior_enum.Safe.value,
        'E': behavior_enum.PDI.value,
        'F': behavior_enum.PDII.value,
        'G': behavior_enum.EI.value,
        'H': behavior_enum.EII.value,
        'I': behavior_enum.VPThreats.value,
        'J': behavior_enum.Aggression.value,
        'K': behavior_enum.Opposition.value
    }

    row2timeperiod = {
        '4':  time_period_enum.TimePeriod01.value,
        '5':  time_period_enum.TimePeriod02.value,
        '6':  time_period_enum.TimePeriod03.value,
        '7':  time_period_enum.TimePeriod04.value,
        '8':  time_period_enum.TimePeriod05.value,
        '9':  time_period_enum.TimePeriod06.value,
        '10': time_period_enum.TimePeriod07.value,
        '11': time_period_enum.TimePeriod08.value,
        '12': time_period_enum.TimePeriod09.value,
        '13': time_period_enum.TimePeriod10.value
    }

    workbook = load_workbook(excel_file)
    worksheet = workbook.active

    ##
    ## This is primarily a data validation ste[
    ##

    # We can't add an IRS for a child that doesn't exist
    student_id = worksheet['B1'].value
    try:
        child = session.query(schema.Child).filter_by(ChildStudentIDN = student_id).one()    
    except NoResultFound:
        logger.error("Child with student ID {0} not found in database. Can't enter IRS for a child that doesn't yet exist.".format(student_id))
        session.rollback()
        session.close()
        return

    logger.debug("Initializing an IRS for child with student IDN {0}".format(student_id))

    # We won't add a second IRS for a child on the same day. That's a no-op
    irs_date = worksheet['L4'].value
    irs_date_int = Date_2_Int(irs_date)
    logger.debug("Creating an IRS for child with student IDN {0} for date {1}".format(student_id, irs_date))
    try:
        irs = session.query(schema.IRS).filter_by(Child = child, IRSDate = irs_date_int).one()
    except NoResultFound:
        # good, we didn't want there to already be an existing value here
        irs = schema.IRS(IRSDate = irs_date_int, Child = child)
        session.add(irs)
    else:
        # Bad news, we aren't going to deal with
        # The same child having two IRS for the same day
        logger.error("Child with student ID {0} already has an IRS for date {1}. Won't enter two IRS for the same date.".format(student_id, irs_date))
        session.rollback()
        session.close()
        return


    ##
    ## Time for the serious data entry
    ##

    # Iterate over the rows and columns
    # and add their values into the BehaviorElement database
    for row, timeperiod in row2timeperiod.items():
        for col, behavior in col2behavior.items():
            
            behaviorelementvalue = worksheet['{0}{1}'.format(col,row)].value
            
            be = schema.BehaviorElement(IRS = irs, Behavior = behavior, TimePeriod = timeperiod, BehaviorElementValue = behaviorelementvalue)
            session.add(be)

            logger.debug("Adding behavior element {0} to irs {1}".format(be, irs))
    try:
        session.commit()
    except BaseException as e:
        logger.exception("Unknown error committing session to database. Rolling back and making no changes.")
        session.rollback()
        
    session.close()
    return
    
