from database import Base
from sqlalchemy import Column, Integer, String, PickleType, Date, Boolean


class Ledgers(Base):
    __tablename__ = 'ledgers'

    #TODO: quitar debits y credits. Dejar solo una variable con los datos económicos

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    ledger_date = Column(Date)
    debits = Column(PickleType)
    credits = Column(PickleType)

class Accounts(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nature = Column(String) #Indicates the nature: assets, liabilities, equity
    status = Column(Boolean, default=True) #Indicates if it's active or inactive

