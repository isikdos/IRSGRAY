import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.schema import ForeignKeyConstraint, UniqueConstraint, Index
from sqlalchemy.orm import relationship
import time

Base = declarative_base()

PRIMARY_KEY_KWARGS = {
                      "type_": Integer,
                      "primary_key": True,
                      "autoincrement": True,
                      "nullable": False,
                      "unique": True
                     }

class Child(Base):
    __tablename__ = "Child"
 
    ChildID = Column(name = "ChildID", **PRIMARY_KEY_KWARGS)
    ChildFirstName = Column(name = "ChildFirstName", type_ = String, nullable = False)
    ChildLastName = Column(name = "ChildLastName", type_ = String, nullable = False)
    ChildMiddleName = Column(name = "ChildMiddleName", type_ = String, nullable = True)
    ChildStudentIDN = Column(name = "ChildStudentIDN", type_ = String, nullable = False, unique = True)

    IRSs = relationship("IRS", back_populates="Child")

    Index('idx_Child_ChildStudentID_ok', ChildStudentIDN)

    def __repr__(self):
        return "<Child(ChildFirstName='{0}', ChildLastName='{1}', ChildMiddleName='{2}', ChildStudentIDN='{3}')>".format(ChildFirstName, ChildLastName, ChildMiddleName, ChildStudentIDN)

    def __str__(self):
        return self.__repr__()


class IRS(Base):
    __tablename__ = "IRS"

    IRSID = Column(name = "IRSID", **PRIMARY_KEY_KWARGS)
    ChildID = Column(name = "ChildID", type_ = Integer, nullable = False)
    IRSDate = Column(name = "IRSDate", type_ = Integer, nullable = False)

    ForeignKeyConstraint(
        [ChildID], [Child.ChildID]
    )

    UniqueConstraint(
        ChildID, IRSDate
    )

    Child = relationship("Child", back_populates="IRSs")
    BehaviorElements = relationship("BehaviorElement", back_populates="IRS")

    Index('idx_IRS_ChildID_fk', ChildID)
    Index('idx_IRS_IRSDate_ChildID_ok', IRSDate, ChildID)

    def __repr__(self):
        return "<IRS(ChildID='{0}', IRSDate='{1}')>".format(self.ChildID, self.IRSDate)

    def __str__(self):
        return self.__repr__()

class TimePeriod(Base):
    __tablename__ = "TimePeriod"

    TimePeriodID = Column(name = "TimePeriodID", **PRIMARY_KEY_KWARGS)
    TimePeriodStartTime = Column(name = "TimePeriodStartTime", type_ = Integer, nullable = False)
    TimePeriodEndTime = Column(name = "TimePeriodEndTime", type_ = Integer, nullable = False)

    def __repr__(self):
        return "<TimePeriod(TimePeriodStartTime='{0}', TimePeriodEndTime='{1}')>".format(self.TimePeriodStartTime, self.TimePeriodEndTime)

    def __str__(self):
        return self.__repr__()



class Behavior(Base):
    __tablename__ = "Behavior"
    
    BehaviorID = Column(name = "BehaviorID", **PRIMARY_KEY_KWARGS) 
    BehaviorName = Column(name = "BehaviorName", type_ = String,  nullable = False, unique = True)
    BehaviorIsPositive = Column(name = "BehaviorIsPositive", type_ = Boolean,  nullable = False)    

    def __repr__(self):
        return "<Behavior(Name='{0}', IsPositive='{1}')>".format(self.BehaviorName, self.BehaviorIsPositive)

    def __str__(self):
        return self.__repr__()



class BehaviorElement(Base):
    __tablename__ = "BehaviorElement"

    BehaviorElementID = Column(name = "BehaviorElementID", **PRIMARY_KEY_KWARGS)
    IRSID = Column(name = "IRSID", type_ = Integer, nullable = False)
    BehaviorID = Column("BehaviorID", type_ = Integer, nullable = False)
    TimePeriodID = Column("TimePeriodID", type_ = Integer, nullable = False)
    BehaviorElementValue = Column("BehaviorElementValue", type_ = Integer, nullable = False, default = 0)

    ForeignKeyConstraint(
        [IRSID], [IRS.IRSID]
    )
    ForeignKeyConstraint(
        [BehaviorID], [Behavior.BehaviorID]
    )
    ForeignKeyConstraint(
        [TimePeriodID], [TimePeriod.TimePeriodID]
    )

    IRS = relationship("IRS", back_populates="BehaviorElements")
    Behavior = relationship("Behavior")
    TimePeriod = relationship("TimePeriod")

    Index('idx_BehaviorElement_BehaviorID_fk', BehaviorID)
    Index('idx_BehaviorElement_IRSID_fk', IRSID)
    Index('idx_BehaviorElement_TimePeriodID_fk', TimePeriodID)

    def __repr__(self):
        return "<BehaviorElement(IRSID='{0}', BehaviorID='{1}', TimePeriodID='{2}', BehaviorElementValue={3})>".format(self.IRSID, self.BehaviorID, self.TimePeriodID, self.BehaviorElementValue)

    def __str__(self):
        return self.__repr__()


class ImportedFile(Base):
    __tablename__ = "ImportedFile"

    ImportedFileID = Column(name = "ImportedFileID", **PRIMARY_KEY_KWARGS)
    ImportedFileFullPath = Column(name = "ImportedFileFullPath", type_ = Integer, nullable = False, unique = True)
    ImportedFileFileName = Column(name = "ImportedFileFileName", type_ = Integer, nullable = False)
    ImportedFileInsertTime = Column(name = "ImportedFileInsertTime", type_ = Integer, nullable = False, default = int(time.time()))

    Index('idx_ImportedFile_ImportedFileFileName_ok', ImportedFileFileName)
    Index('idx_ImportedFile_ImportedFileFullPath_ok', ImportedFileFullPath)

    def __repr__(self):
        return "<ImportedFile(ImportedFileFullPath='{0}', ImportedFileFileName='{1}')>".format(self.ImportedFileFullPath, self.ImportedFileFileName)

    def __str__(self):
        return self.__repr__()

