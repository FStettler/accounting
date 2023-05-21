from database import Base
from sqlalchemy import Column, Integer, String, PickleType, Date, Boolean, ForeignKey


class Ledgers(Base):
    __tablename__ = 'ledgers'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    ledger_date = Column(Date)
    debits = Column(PickleType)
    credits = Column(PickleType)
    user_id = Column(Integer, ForeignKey("users.id"))

class Accounts(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer)
    name = Column(String)
    nature = Column(String) #Indicates the nature: assets, liabilities, equity
    status = Column(Boolean, default=True) #Indicates if it's active or inactive
    user_id = Column(Integer, ForeignKey("users.id"))

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    status = Column(Boolean, default=True)
    role = Column(String)