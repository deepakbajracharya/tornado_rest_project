from datetime import datetime

from sqlalchemy import (Column, Integer, DateTime, Unicode)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Widget(Base):
    __tablename__ = 't_widget'

    id              = Column(Integer,
                             primary_key   = True,
                             autoincrement = True)
    # Unique not enforce # unique=True
    name            = Column(Unicode(64),
                             nullable=False)
    number_of_parts = Column(Integer, nullable=False)
    created_date    = Column(DateTime(), default=datetime.utcnow)
    updated_date    = Column(DateTime(),
                             default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return ("<Widget id: {}, name: {}, number_of_parts: {},"
                "created_date: {}, updated_date: {}".format(
                    self.id, self.name, self.number_of_parts,
                    self.created_date, self.updated_date))
