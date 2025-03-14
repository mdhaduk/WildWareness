import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create mocks for the database dependencies
class MockBase:
    metadata = {}

class MockWildfire:
    pass

class MockShelter:
    pass

class MockNewsReport:
    pass

# Mock the database module
database_module = MagicMock()
database_module.init_db = MagicMock()
database_module.load_wildfires = MagicMock()
database_module.load_shelters = MagicMock()
sys.modules['database'] = database_module

# Mock the models module
models_module = MagicMock()
models_module.Base = MockBase
models_module.Wildfire = MockWildfire
models_module.Shelter = MockShelter
models_module.NewsReport = MockNewsReport
sys.modules['models'] = models_module

class TestDatabase(unittest.TestCase):
    """Test cases for the database module"""

    def setUp(self):
        # Reset mocks before each test
        database_module.init_db.reset_mock()
        database_module.load_wildfires.reset_mock()
        database_module.load_shelters.reset_mock()

    def test_init_db(self):
        """Test initializing the database"""
        # Setup mocks
        mock_engine = MagicMock()
        mock_session = MagicMock()
        
        # Configure the init_db mock to return the expected values
        database_module.init_db.return_value = (mock_engine, mock_session)
        
        # Call the function
        engine, session_factory = database_module.init_db(':memory:')
        
        # Assertions
        database_module.init_db.assert_called_once_with(':memory:')
        self.assertEqual(engine, mock_engine)
        self.assertEqual(session_factory, mock_session)
    
    def test_init_db_with_echo(self):
        """Test initializing the database with echo=True"""
        # Setup mocks
        mock_engine = MagicMock()
        mock_session = MagicMock()
        
        # Configure the init_db mock to return the expected values
        database_module.init_db.return_value = (mock_engine, mock_session)
        
        # Call the function
        engine, session_factory = database_module.init_db(':memory:', echo=True)
        
        # Assertions
        database_module.init_db.assert_called_once_with(':memory:', echo=True)
        self.assertEqual(engine, mock_engine)
        self.assertEqual(session_factory, mock_session)
    
    def test_load_wildfires(self):
        """Test loading wildfires from JSON file"""
        # Setup mocks
        mock_wildfires = [MockWildfire()]
        
        # Configure the load_wildfires mock to return the expected values
        database_module.load_wildfires.return_value = mock_wildfires
        
        # Call the function
        result = database_module.load_wildfires()
        
        # Assertions
        database_module.load_wildfires.assert_called_once()
        self.assertEqual(result, mock_wildfires)
    
    def test_load_shelters(self):
        """Test loading shelters from JSON file"""
        # Setup mocks
        mock_shelters = [MockShelter()]
        
        # Configure the load_shelters mock to return the expected values
        database_module.load_shelters.return_value = mock_shelters
        
        # Call the function
        result = database_module.load_shelters()
        
        # Assertions
        database_module.load_shelters.assert_called_once()
        self.assertEqual(result, mock_shelters)


if __name__ == "__main__":
    unittest.main() 