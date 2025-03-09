from sqlalchemy import Integer, String, Column, JSON, Text, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, relationship
import json


TESTING = True

class Base(DeclarativeBase):
    pass

Wildfire_Shelter = Table(
    "wildfires_shelters",
    Base.metadata,
    Column("wildfires_id", Integer, ForeignKey("wildfires.id"), primary_key=True),
    Column("shelters_id", Integer, ForeignKey("shelters.id"), primary_key=True),
)



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

    # shelters = relationship(
    #     "Shelter", secondary=Wildfire_Shelter, back_populates="shelters"
    # )

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

class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    website = Column(Text, nullable=False)
    rating = Column(Text, nullable=False)
    reviews = Column(JSON, nullable=False, default=list)
    imageUrl = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    # wildfires = relationship(
    #     "Wildfire", secondary=Wildfire_Shelter, back_populates="wildfires"
    # )

    def as_instance(self):
        instance = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "website": self.website,
            "rating": self.rating,
            "reviews": self.reviews,
            "imageUrl": self.imageUrl,
            "description": self.description

        }
        return instance
