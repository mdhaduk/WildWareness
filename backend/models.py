from sqlalchemy import Integer, String, Column, JSON, Text, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, relationship
import json

TESTING = True


class Base(DeclarativeBase):
    pass


class Wildfire(Base):
    __tablename__ = "wildfires"
    # card
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    county = Column(Text, nullable=False)
    location = Column(Text, nullable=False)
    date = Column(Text, nullable=False)
    acres_burned = Column(Text, nullable=False)
    images = Column(JSON, nullable=False, default=list)

    def as_instance(self):
        instance = {
            "id": self.id,
            "name": self.name,
            "county": self.county,
            "location": self.location,
            "date": self.date,
            "acres_burned": self.acres_burned,
            "images": self.images
        }
        return instance
