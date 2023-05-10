from database import Base
from sqlalchemy import Column, Integer, String, PickleType, Date


class Ledgers(Base):
    __tablename__ = 'ledgers'

    #TODO: quitar debits y credits. Dejar solo una variable con los datos económicos

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    ledger_date = Column(Date)
    debits = Column(PickleType)
    credits = Column(PickleType)


