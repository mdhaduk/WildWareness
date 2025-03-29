from sqlalchemy import Integer, String, Float, Column, JSON, Text, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, relationship
import json
from scripts.helper_scripts import get_county_from_address


TESTING = True

class Base(DeclarativeBase):
    pass

Wildfire_Shelter = Table(
    "wildfires_shelters",
    Base.metadata,
    Column("wildfires_id", Integer, ForeignKey("wildfires.id", ondelete="CASCADE"), primary_key=True),
    Column("shelters_id", Integer, ForeignKey("shelters.id", ondelete="CASCADE"), primary_key=True),
)

Wildfire_NewsReport = Table(
    "wildfires_newsreports",
    Base.metadata,
    Column("wildfires_id", Integer, ForeignKey("wildfires.id", ondelete="CASCADE"), primary_key=True),
    Column("news_id", Integer, ForeignKey("news.id", ondelete="CASCADE"), primary_key=True),
)

Shelter_NewsReport = Table(
    "shelters_newsreports",
    Base.metadata,
    Column("shelters_id", Integer, ForeignKey("shelters.id", ondelete="CASCADE"), primary_key=True),
    Column("news_id", Integer, ForeignKey("news.id", ondelete="CASCADE"), primary_key=True),
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
    status = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    latitude = Column(Text, nullable=False)
    longitude = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    shelters = relationship(
        "Shelter", secondary=Wildfire_Shelter, back_populates="wildfires"
    )

    newsreports = relationship(
        "NewsReport", secondary=Wildfire_NewsReport, back_populates="wildfires"
    )

    def as_instance(self):
        instance = {
            "id": self.id,
            "name": self.name,
            "county": self.county,
            "location": self.location,
            "year": self.year,
            "acres_burned": self.acres_burned,
            "status": self.status,
            "url": self.url,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "description": self.description,
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

class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    county = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    website = Column(Text, nullable=False)
    rating = Column(Text, nullable=False)
    reviews = Column(JSON, nullable=False, default=list)
    imageUrl = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    wildfires = relationship(
        "Wildfire", secondary=Wildfire_Shelter, back_populates="shelters"
    )

    newsreports = relationship(
        "NewsReport", secondary=Shelter_NewsReport, back_populates="shelters"
    )

    def as_instance(self):
        instance = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "county": self.county,
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


class NewsReport(Base):
    __tablename__ = "news"
    # card
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=False)  # Store list of keywords as a JSON array
    snippet = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    image_url = Column(Text, nullable=False)
    language = Column(Text, nullable=True)
    published_at = Column(Text, nullable=True)
    source = Column(Text, nullable=True)
    categories = Column(Text, nullable=False)  # Store list of categories as a JSON array
    relevance_score = Column(Float, nullable=True)
    search_query = Column(Text, nullable=True)
    author = Column(Text, nullable=True)
    locations = Column(JSON, nullable=False)  # Store list of locations as a JSON array
    geo_locations = Column(JSON, nullable=False)  # Store list of geo-location objects as JSON
    map_urls = Column(JSON, nullable=False)  # Store list of map URLs as JSON
    reading_time = Column(Integer, nullable=False)
    socials = Column(JSON, nullable=False)  # Store list of social URLs as JSON
    text_summary = Column(Text, nullable=False)
    related_articles = Column(JSON, nullable=False)  # Store list of related articles as JSON
    hashtag_links = Column(JSON, nullable=False)  # Store list of hashtag links as JSON
    images = Column(JSON, nullable=False)  # Store list of images as JSON
    videos = Column(JSON, nullable=False)  # Store list of videos as JSON
    county = Column(JSON, nullable=False)

    wildfires = relationship(
        "Wildfire", secondary=Wildfire_NewsReport, back_populates="newsreports"
    )

    shelters = relationship(
        "Shelter", secondary=Shelter_NewsReport, back_populates="newsreports"
    )

    def as_instance(self):
        instance = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "snippet": self.snippet,
            "url": self.url,
            "image_url": self.image_url,
            "language": self.language,
            "published_at": self.published_at,
            "source": self.source,
            "categories": self.categories,
            "relevance_score": self.relevance_score,
            "search_query": self.search_query,
            "author": self.author,
            "locations": self.locations,
            "geo_locations": self.geo_locations,
            "map_urls": self.map_urls,
            "reading_time": self.reading_time,
            "socials": self.socials,
            "text_summary": self.text_summary,
            "related_articles": self.related_articles,
            "hashtag_links": self.hashtag_links,
            "images": self.images,
            "videos": self.videos,
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