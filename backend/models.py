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
    year = Column(Text, nullable=False)
    acres_burned = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    latitude = Column(Text, nullable=False)
    longitude = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    def as_instance(self):
        instance = {
            "id": self.id,
            "name": self.name,
            "county": self.county,
            "location": self.location,
            "year": self.year,
            "acres_burned": self.acres_burned,
            "url": self.url,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "description": self.description
        }
        return instance
