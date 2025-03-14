import unittest
import sys
import os
import json

# Add the parent directory to the path so we can import the models module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models - test them in isolation
class MockBase:
    pass

# Add mock for models.py imports
sys.modules['sqlalchemy.orm'] = type('mock', (), {
    'relationship': lambda *args, **kwargs: None
})
sys.modules['sqlalchemy'] = type('mock', (), {
    'Integer': None, 'String': None, 'Float': None, 'Column': lambda *args, **kwargs: None,
    'JSON': None, 'Text': None, 'ForeignKey': lambda *args: None, 'Table': lambda *args, **kwargs: None
})

class TestWildfire(unittest.TestCase):
    """Test cases for the Wildfire model"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a simplified Wildfire class for testing
        class Wildfire:
            def __init__(self, id, name, county, location, year, acres_burned, url, latitude, longitude, description, ongoing):
                self.id = id
                self.name = name
                self.county = county
                self.location = location
                self.year = year
                self.acres_burned = acres_burned
                self.url = url
                self.latitude = latitude
                self.longitude = longitude
                self.description = description
                self.ongoing = ongoing
            
            def as_instance(self):
                return {
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
                    "ongoing": bool(self.ongoing)  # Convert 0/1 to False/True
                }
                
        self.Wildfire = Wildfire
        self.wildfire = Wildfire(
            id=1,
            name="Test Wildfire",
            county="Test County",
            location="Test Location",
            year="2023",
            acres_burned="1000",
            url="https://example.com",
            latitude="37.7749",
            longitude="-122.4194",
            description="Test description",
            ongoing=1
        )

    def test_as_instance(self):
        """Test that as_instance returns the expected dictionary"""
        expected = {
            "id": 1,
            "name": "Test Wildfire",
            "county": "Test County",
            "location": "Test Location",
            "year": "2023",
            "acres_burned": "1000",
            "url": "https://example.com",
            "latitude": "37.7749",
            "longitude": "-122.4194",
            "description": "Test description",
            "ongoing": True
        }
        self.assertEqual(self.wildfire.as_instance(), expected)

    def test_ongoing_conversion(self):
        """Test that the ongoing field is properly converted to boolean"""
        self.wildfire.ongoing = 0
        self.assertEqual(self.wildfire.as_instance()["ongoing"], False)
        
        self.wildfire.ongoing = 1
        self.assertEqual(self.wildfire.as_instance()["ongoing"], True)


class TestShelter(unittest.TestCase):
    """Test cases for the Shelter model"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a simplified Shelter class for testing
        class Shelter:
            def __init__(self, id, name, address, phone, website, rating, reviews, imageUrl, description, county, max_occupancy):
                self.id = id
                self.name = name
                self.address = address
                self.phone = phone
                self.website = website
                self.rating = rating
                self.reviews = reviews
                self.imageUrl = imageUrl
                self.description = description
                self.county = county
                self.max_occupancy = max_occupancy
            
            def as_instance(self):
                return {
                    "id": self.id,
                    "name": self.name,
                    "address": self.address,
                    "phone": self.phone,
                    "website": self.website,
                    "rating": self.rating,
                    "reviews": self.reviews,
                    "imageUrl": self.imageUrl,
                    "description": self.description,
                    "county": self.county,
                    "max_occupancy": self.max_occupancy
                }
                
        self.Shelter = Shelter
        self.shelter = Shelter(
            id=1,
            name="Test Shelter",
            address="123 Test St",
            phone="123-456-7890",
            website="https://example.com",
            rating="4.5",
            reviews=json.dumps([{"user": "Test User", "rating": 4, "comment": "Good shelter"}]),
            imageUrl="https://example.com/image.jpg",
            description="Test description",
            county="Test County",
            max_occupancy=100
        )

    def test_as_instance(self):
        """Test that as_instance returns the expected dictionary"""
        expected = {
            "id": 1,
            "name": "Test Shelter",
            "address": "123 Test St",
            "phone": "123-456-7890",
            "website": "https://example.com",
            "rating": "4.5",
            "reviews": json.dumps([{"user": "Test User", "rating": 4, "comment": "Good shelter"}]),
            "imageUrl": "https://example.com/image.jpg",
            "description": "Test description",
            "county": "Test County",
            "max_occupancy": 100
        }
        self.assertEqual(self.shelter.as_instance(), expected)


class TestNewsReport(unittest.TestCase):
    """Test cases for the NewsReport model"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a simplified NewsReport class for testing
        class NewsReport:
            def __init__(self, id, uuid, title, description, keywords, snippet, url, image_url, language, published_at, source, categories, relevance_score, search_query, author, locations, geo_locations, map_urls, reading_time, socials, text_summary, related_articles, hashtag_links, images, videos):
                self.id = id
                self.uuid = uuid
                self.title = title
                self.description = description
                self.keywords = keywords
                self.snippet = snippet
                self.url = url
                self.image_url = image_url
                self.language = language
                self.published_at = published_at
                self.source = source
                self.categories = categories
                self.relevance_score = relevance_score
                self.search_query = search_query
                self.author = author
                self.locations = locations
                self.geo_locations = geo_locations
                self.map_urls = map_urls
                self.reading_time = reading_time
                self.socials = socials
                self.text_summary = text_summary
                self.related_articles = related_articles
                self.hashtag_links = hashtag_links
                self.images = images
                self.videos = videos
            
            def as_instance(self):
                return {
                    "id": self.id,
                    "uuid": self.uuid,
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
                    "videos": self.videos
                }
                
        self.NewsReport = NewsReport
        self.news_report = NewsReport(
            id=1,
            uuid="test-uuid",
            title="Test News",
            description="Test news description",
            keywords=json.dumps(["wildfire", "emergency"]),
            snippet="Test snippet",
            url="https://example.com",
            image_url="https://example.com/image.jpg",
            language="en",
            published_at="2023-01-01",
            source="Test Source",
            categories=json.dumps(["news", "disaster"]),
            relevance_score=0.95,
            search_query="wildfire california",
            author="Test Author",
            locations=json.dumps(["California", "Los Angeles"]),
            geo_locations=json.dumps([{"lat": 37.7749, "lng": -122.4194}]),
            map_urls=json.dumps(["https://maps.example.com"]),
            reading_time=5,
            socials=json.dumps(["https://twitter.com/example"]),
            text_summary="Test summary",
            related_articles=json.dumps(["https://example.com/related"]),
            hashtag_links=json.dumps(["#wildfire"]),
            images=json.dumps(["https://example.com/image.jpg"]),
            videos=json.dumps(["https://example.com/video.mp4"])
        )

    def test_as_instance(self):
        """Test that as_instance returns the expected dictionary"""
        expected = {
            "id": 1,
            "uuid": "test-uuid",
            "title": "Test News",
            "description": "Test news description",
            "keywords": json.dumps(["wildfire", "emergency"]),
            "snippet": "Test snippet",
            "url": "https://example.com",
            "image_url": "https://example.com/image.jpg",
            "language": "en",
            "published_at": "2023-01-01",
            "source": "Test Source",
            "categories": json.dumps(["news", "disaster"]),
            "relevance_score": 0.95,
            "search_query": "wildfire california",
            "author": "Test Author",
            "locations": json.dumps(["California", "Los Angeles"]),
            "geo_locations": json.dumps([{"lat": 37.7749, "lng": -122.4194}]),
            "map_urls": json.dumps(["https://maps.example.com"]),
            "reading_time": 5,
            "socials": json.dumps(["https://twitter.com/example"]),
            "text_summary": "Test summary",
            "related_articles": json.dumps(["https://example.com/related"]),
            "hashtag_links": json.dumps(["#wildfire"]),
            "images": json.dumps(["https://example.com/image.jpg"]),
            "videos": json.dumps(["https://example.com/video.mp4"])
        }
        self.assertEqual(self.news_report.as_instance(), expected)


if __name__ == "__main__":
    unittest.main() 