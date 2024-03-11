from sqlalchemy import Integer, String, Column, ForeignKey, Boolean
from database import Base

class Wrestlers(Base):
    __tablename__ = 'wrestlers'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))


class Actions(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))


class Techniques(Base):
    __tablename__ = 'techniques'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    action_id = Column(Integer, ForeignKey("actions.id"))


class Wrests(Base):
    __tablename__ = 'wrests'
    
    id = Column(Integer, primary_key=True, index=True)
    wrestler_id = Column(Integer, ForeignKey("wrestlers.id"))
    opponent_id = Column(Integer, ForeignKey("wrestlers.id"))


class Authors(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class Records(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True, index=True)
    second = Column(String(20))
    successful = Column(Boolean)
    score = Column(Integer)
    defense = Column(Boolean)
    flag = Column(Boolean, default=False)
    wrest_id = Column(Integer, ForeignKey("wrests.id"))
    technique_id = Column(Integer, ForeignKey("techniques.id"))
    author_id = Column(Integer, ForeignKey("authors.id"))
    status = Column(Integer, ForeignKey("status.id"))