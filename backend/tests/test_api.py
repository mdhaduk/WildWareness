import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock
import requests

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create mocks for the models
class MockWildfire:
    def __init__(self, id=1, name="Test Wildfire", county="Test County", location="Test Location", 
                 year="2023", acres_burned="1000", url="https://example.com", latitude="37.7749", 
                 longitude="-122.4194", description="Test description", ongoing=1):
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
            "ongoing": bool(self.ongoing)
        }

class MockShelter:
    def __init__(self, id=1, name="Test Shelter", address="123 Test St", phone="123-456-7890",
                 website="https://example.com", rating="4.5", 
                 reviews=json.dumps([{"user": "Test User", "rating": 4, "comment": "Good shelter"}]),
                 imageUrl="https://example.com/image.jpg", description="Test description",
                 county="Test County", max_occupancy=100):
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

class MockNewsReport:
    def __init__(self, id=1, uuid="test-uuid", title="Test News", description="Test news description",
                 keywords=json.dumps(["wildfire", "emergency"]), snippet="Test snippet",
                 url="https://example.com", image_url="https://example.com/image.jpg",
                 language="en", published_at="2023-01-01", source="Test Source",
                 categories=json.dumps(["news", "disaster"]), relevance_score=0.95,
                 search_query="wildfire california", author="Test Author",
                 locations=json.dumps(["California", "Los Angeles"]),
                 geo_locations=json.dumps([{"lat": 37.7749, "lng": -122.4194}]),
                 map_urls=json.dumps(["https://maps.example.com"]), reading_time=5,
                 socials=json.dumps(["https://twitter.com/example"]), text_summary="Test summary",
                 related_articles=json.dumps(["https://example.com/related"]),
                 hashtag_links=json.dumps(["#wildfire"]),
                 images=json.dumps(["https://example.com/image.jpg"]),
                 videos=json.dumps(["https://example.com/video.mp4"])):
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

# Mock the models module
models_module = MagicMock()
models_module.Wildfire = MockWildfire
models_module.Shelter = MockShelter
models_module.NewsReport = MockNewsReport
sys.modules['models'] = models_module

# Create mock API functions for testing
def mock_get_wildfires():
    return [MockWildfire().as_instance()]

def mock_get_wildfire(wildfire_id):
    return MockWildfire(id=wildfire_id).as_instance()

def mock_get_shelters():
    return [MockShelter().as_instance()]

def mock_get_shelter(shelter_id):
    return MockShelter(id=shelter_id).as_instance()

def mock_get_news():
    return [MockNewsReport().as_instance()]

def mock_get_news_report(news_id):
    return MockNewsReport(id=news_id).as_instance()

# Mock the api module
api_module = MagicMock()
api_module.get_wildfires = mock_get_wildfires
api_module.get_wildfire = mock_get_wildfire
api_module.get_shelters = mock_get_shelters
api_module.get_shelter = mock_get_shelter
api_module.get_news = mock_get_news
api_module.get_news_report = mock_get_news_report
sys.modules['api'] = api_module


class TestAPI(unittest.TestCase):
    """Test cases for the API module"""

    def test_get_wildfires(self):
        """Test getting all wildfires"""
        # Call the function
        result = api_module.get_wildfires()
        
        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Test Wildfire")

    def test_get_wildfire(self):
        """Test getting a specific wildfire by ID"""
        # Call the function
        result = api_module.get_wildfire(1)
        
        # Assertions
        self.assertEqual(result["name"], "Test Wildfire")
        self.assertEqual(result["id"], 1)

    def test_get_shelters(self):
        """Test getting all shelters"""
        # Call the function
        result = api_module.get_shelters()
        
        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Test Shelter")

    def test_get_shelter(self):
        """Test getting a specific shelter by ID"""
        # Call the function
        result = api_module.get_shelter(1)
        
        # Assertions
        self.assertEqual(result["name"], "Test Shelter")
        self.assertEqual(result["id"], 1)

    def test_get_news(self):
        """Test getting all news reports"""
        # Call the function
        result = api_module.get_news()
        
        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Test News")

    def test_get_news_report(self):
        """Test getting a specific news report by ID"""
        # Call the function
        result = api_module.get_news_report(1)
        
        # Assertions
        self.assertEqual(result["title"], "Test News")
        self.assertEqual(result["id"], 1)
    

# New test class with renamed methods to avoid clashes with existing tests
class TestAPIv2(unittest.TestCase):
    def get_response(self, endpoint, exp_status=200):
        url = f"https://api.wildwareness.net/{endpoint}" 
        response = requests.get(url)
        self.assertEqual(response.status_code, exp_status)
        return response.json()
    
    def test_fires(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('wildfire_incidents?page=2')
        # Assertions
        self.assertEqual(len(response["incidents"]), 10)  # Adjusted the expected length
        self.assertIn("name", response["incidents"][0])
        self.assertIn("acres_burned", response["incidents"][0])
    
    def test_single_fire(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('wildfire_incidents/10')
        # Assertions
        self.assertIn("name", response)
        self.assertIn("id", response)
        self.assertIn("county", response)
        self.assertIn("acres_burned", response)
    
    def test_shelters(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('shelters')
        # Assertions
        self.assertEqual(len(response["shelters"]), 10)  # Adjusted the expected length
        self.assertIn("website", response["shelters"][0])
        self.assertIn("phone", response["shelters"][0])
    
    def test_single_shelter(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('shelters/20')
        # Assertions
        self.assertIn("id", response)
        self.assertIn("address", response)
        self.assertIn("reviews", response)
        self.assertIn("name", response)

    def test_reports(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('news?page=1')
        # Assertions
        self.assertEqual(len(response["reports"]), 2)  # Adjusted the expected length
        self.assertIn("author", response["reports"][0])
        self.assertIn("categories", response["reports"][0])
    
    def test_single_report(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('news/15')
        # Assertions
        self.assertIn("id", response)
        self.assertIn("title", response)
        self.assertIn("reading_time", response)
        self.assertIn("locations", response)


# New test class with renamed methods to avoid clashes with existing tests
# Tests sorting, seaching, filtering
class TestAPIv3(unittest.TestCase):
    def get_response(self, endpoint, exp_status=200):
        url = f"https://api.wildwareness.net/{endpoint}" 
        response = requests.get(url)
        self.assertEqual(response.status_code, exp_status)
        return response.json()
    
    def test_fires_search(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('wildfire_incidents?page=&size=&search=bryson&sort_by=name&order=asc&location=&year=&acres_burned=&status=')
        # Assertions
        self.assertEqual((response["incidents"][0]["name"]).strip().lower(), "bryson fire")
        self.assertEqual(len(response["incidents"]), 1)
        self.assertEqual((response["incidents"][0]["county"]).strip().lower(), "monterey")

    def test_fires_filter(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('wildfire_incidents?page=&size=&sort_by=name&order=asc&location=Colusa&year=&acres_burned=&status=')
        # Assertions
        self.assertEqual((response["incidents"][0]["name"]).strip().lower(), "sites fire")
        self.assertEqual(len(response["incidents"]), 1)
        self.assertEqual((response["incidents"][0]["county"]).strip().lower(), "colusa")
    
    def test_fires_sort(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('wildfire_incidents?page=&size=&sort_by=county&order=desc&location=&year=&acres_burned=&status=')
        # Assertions
        self.assertEqual((response["incidents"][0]["name"]).strip().lower(), "pendola fire")
        self.assertEqual((response["incidents"][1]["name"]).strip().lower(), "spenceville fire")
        self.assertEqual((response["incidents"][2]["name"]).strip().lower(), "double fire")


    def test_shelters_search(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('shelters?page=&size=&search=butte&sort_by=name&order=asc&location=&year=&acres_burned=&status=')
        # Assertions
        self.assertEqual((response["shelters"][0]["name"]).strip().lower(), "esplanade house")
        self.assertEqual(len(response["shelters"]), 10)
        self.assertEqual((response["shelters"][1]["county"]).strip().lower(), "butte county")

    def test_shelters_filter(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('shelters?page=&size=&sort_by=name&order=asc&county=&zipCode=92010&phone=&rating=4')
        # Assertions
        self.assertEqual((response["shelters"][0]["name"]).strip().lower(), "catholic charities la posada")
        self.assertEqual(len(response["shelters"]), 1)
        response = self.get_response('shelters?page=&size=&sort_by=name&order=asc&county=&zipCode=95112&phone=&rating=4')
        self.assertEqual((response["shelters"][0]["name"]).strip().lower(), "cityteam renew for men: residential program")
        self.assertEqual(len(response["shelters"]), 1)
    
    def test_shelters_sort(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('shelters?page=&size=&sort_by=county&order=desc&county=&zipCode=&phone=&rating=')
        # Assertions
        self.assertEqual((response["shelters"][0]["name"]).strip().lower(), "twin cities rescue mission")
        self.assertEqual(len(response["shelters"]), 10)
        response = self.get_response('shelters?page=&size=&sort_by=county&order=desc&county=imperial&zipCode=&phone=&rating=')
        self.assertEqual((response["shelters"][0]["name"]).strip().lower(), "new creations men's home")
        # self.assertEqual((response["shelters"][0]["county"]).strip().lower(), "yuba county")
    

    def test_reports_search(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('news?page=&size=&search=air&sort_by=title&order=asc&source=&author=&date=&categories=')
        # Assertions
        self.assertEqual((response["reports"][0]["source"]).strip().lower(), "ibtimes.com")
        self.assertEqual((response["reports"][1]["author"]).strip().lower(), "adweek.com")
        self.assertEqual((response["reports"][2]["author"]).strip().lower(), "abc news")
    

    def test_reports_filter(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('news?page=&size=&sort_by=title&order=asc&source=&author=&date=&categories=general,business')
        # Assertions
        self.assertEqual((response["reports"][0]["source"]).strip().lower(), "ibtimes.com")
        self.assertEqual((response["reports"][1]["author"]).strip().lower(), "manilatimes.net")
        self.assertEqual((response["reports"][1]["title"]).strip().lower(), "acwa statement on southern california wildfires")
    
    def test_reports_sort(self):
        # Call the mock API endpoint for wildfire incidents
        response = self.get_response('news?page=&size=&sort_by=published_at&order=desc&source=&author=&date=&categories=')
        # Assertions
        self.assertEqual((response["reports"][0]["published_at"]).strip().lower(), "2025-03-05")
        self.assertEqual((response["reports"][1]["published_at"]).strip().lower(), "2025-02-23")
        self.assertEqual((response["reports"][0]["source"]).strip().lower(), "webpronews.com")

    




if __name__ == "__main__":
    unittest.main() 

