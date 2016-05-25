from sqlalchemy import Column, Integer, String, Text, DateTime
import datetime
from testmanager.database import Base


class Evidence(Base):
    __tablename__ = 'evidence'
    id = Column(Integer, primary_key=True,autoincrement=True)
    id_probe = Column(Integer, nullable=False,unique=False)
    result = Column(String(10), unique=False,nullable=False)
    dtime =Column(DateTime,unique=False,nullable=False)

    def __init__(self, id_probe, result=True,dtime=datetime.datetime.now()):
        self.id_probe=id_probe
        self.result=result
        self.dtime=dtime

    def __repr__(self):
         return '<result %r>' % (self.result)