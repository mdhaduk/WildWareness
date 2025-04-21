from sqlalchemy import Integer, Column, JSON, Text, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, relationship

# Testing
TESTING = False

class Base(DeclarativeBase):
    pass

# For connections between instances of different models
# Association table for relationship between Wildfires and Shelters
Wildfire_Shelter = Table(
    "wildfires_shelters",
    Base.metadata,
    Column("wildfires_id", Integer, ForeignKey("wildfires.id", ondelete="CASCADE"), primary_key=True),
    Column("shelters_id", Integer, ForeignKey("shelters.id", ondelete="CASCADE"), primary_key=True),
)

# Association table between Wildfires and Reports
Wildfire_NewsReport = Table(
    "wildfires_newsreports",
    Base.metadata,
    Column("wildfires_id", Integer, ForeignKey("wildfires.id", ondelete="CASCADE"), primary_key=True),
    Column("news_id", Integer, ForeignKey("news.id", ondelete="CASCADE"), primary_key=True),
)

# Association table between Shelters and Reports
Shelter_NewsReport = Table(
    "shelters_newsreports",
    Base.metadata,
    Column("shelters_id", Integer, ForeignKey("shelters.id", ondelete="CASCADE"), primary_key=True),
    Column("news_id", Integer, ForeignKey("news.id", ondelete="CASCADE"), primary_key=True),
)


# Model for wildfires
class Wildfire(Base):
    __tablename__ = "wildfires"
    # Columns representing attributes of a wildfire
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
    status = Column(Text, nullable=False)

    # Get relationships with shelter and reports models
    shelters = relationship(
        "Shelter", secondary=Wildfire_Shelter, back_populates="wildfires"
    )
    newsreports = relationship(
        "NewsReport", secondary=Wildfire_NewsReport, back_populates="wildfires"
    )

    # Build and return dictionary for a wildfire entry
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
            "description": self.description,
            "status": self.status,
            "shelters": [
                {"id": shelter.id, "name": shelter.name, "address": shelter.address,
                    "phone": shelter.phone, "website": shelter.website, "rating": shelter.rating,
                    "imageUrl": shelter.imageUrl}
                for shelter in self.shelters
            ],
            "newsreports": [
                {"id": news.id, "title": news.title, "source": news.source, "date": news.published_at,
                    "author": news.author, "categories": news.categories, "image_url": news.image_url,}
                for news in self.newsreports
            ],

        }
        return instance


# Model for shelters
class Shelter(Base):
    __tablename__ = "shelters"
    # Columns representing attributes of a shelter
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    website = Column(Text, nullable=False)
    rating = Column(Text, nullable=False)
    reviews = Column(JSON, nullable=False, default=list)
    imageUrl = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    county = Column(Text, nullable=False)

    # Get relationships with wildfire and reports models
    wildfires = relationship(
        "Wildfire", secondary=Wildfire_Shelter, back_populates="shelters"
    )
    newsreports = relationship(
        "NewsReport", secondary=Shelter_NewsReport, back_populates="shelters"
    )

    # Build and return dictionary for a shelter entry
    def as_instance(self):
        instance = {
            "id": self.id,
            "name": self.name,
            "county": self.county,
            "address": self.address,
            "phone": self.phone,
            "website": self.website,
            "rating": self.rating,
            "reviews": self.reviews,
            "imageUrl": self.imageUrl,
            "description": self.description,
            "wildfires": [
                {"id": wildfire.id, "name": wildfire.name, "county": wildfire.county,
                    "location": wildfire.location, "year": wildfire.year, "acres_burned": wildfire.acres_burned,
                    "url": wildfire.url}
                for wildfire in self.wildfires
            ],
            "newsreports": [
                {"id": news.id, "title": news.title, "source": news.source, "date": news.published_at,
                    "author": news.author, "categories": news.categories, "image_url": news.image_url,}
                for news in self.newsreports
            ],
        }
        return instance


# Model for news reports
class NewsReport(Base):
    __tablename__ = "news"
    # Columns representing attributes of a news report
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    image_url = Column(Text, nullable=False)
    published_at = Column(Text, nullable=True)
    source = Column(Text, nullable=True)
    categories = Column(Text, nullable=False)  # Store list of categories as a JSON array
    author = Column(Text, nullable=True)
    locations = Column(JSON, nullable=False)  # Store list of locations as a JSON array
    reading_time = Column(Integer, nullable=False)
    text_summary = Column(Text, nullable=False)
    county = Column(JSON, nullable=False)

    # Get relationships with wildfire and shelters models
    wildfires = relationship(
        "Wildfire", secondary=Wildfire_NewsReport, back_populates="newsreports"
    )
    shelters = relationship(
        "Shelter", secondary=Shelter_NewsReport, back_populates="newsreports"
    )

     # Build and return dictionary for a news reports entry
    def as_instance(self):
        instance = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "image_url": self.image_url,
            "published_at": self.published_at,
            "source": self.source,
            "categories": self.categories,
            "author": self.author,
            "locations": self.locations,
            "reading_time": self.reading_time,
            "text_summary": self.text_summary,
            "county": self.county,
            "wildfires": [
                {"id": wildfire.id, "name": wildfire.name, "county": wildfire.county,
                    "location": wildfire.location, "year": wildfire.year, "acres_burned": wildfire.acres_burned,
                    "url": wildfire.url}
                for wildfire in self.wildfires
            ],
            "shelters": [
                {"id": shelter.id, "name": shelter.name, "address": shelter.address,
                    "phone": shelter.phone, "website": shelter.website, "rating": shelter.rating,
                    "imageUrl": shelter.imageUrl}
                for shelter in self.shelters
            ],
        }
        
        return instance