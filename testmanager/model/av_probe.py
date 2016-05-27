from sqlalchemy import Column, Integer, String, Text

from testmanager.database import Base


class Static_Probe(Base):
    __tablename__ = 'static_probe'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False, unique=False)
    doc = Column(Text(), unique=False, nullable=False)

    def __init__(self, type, doc=None):
        self.type = type
        self.doc = doc

    def __repr__(self):
        return '<User %r>' % (self.name)
