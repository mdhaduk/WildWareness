import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

url = "https://wildwareness.net/"

class FrontendAcceptanceTests(unittest.TestCase):

    def setUp(self):
        """Setup Chrome WebDriver with headless options for CI environments."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run without UI
        chrome_options.add_argument("--no-sandbox")  # Required for Docker
        chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent crashes in limited memory environments
        chrome_options.add_argument("--window-size=1920,1080")  # Set fixed resolution
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url)

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()

    # ✅ Test 1: Navbar Routing
    def test_0_navbar_routing(self):
        """Test that navbar links navigate to the correct pages."""
        nav_links = {
            "Wildfire Incidents": "incidents",
            "Emergency Shelters": "shelters",
            "Community Reports": "news",
            "About": "about",
            "Home": ""
        }

        for link_text, expected_endpoint in nav_links.items():
            button = self.driver.find_element(By.LINK_TEXT, link_text)
            button.click()
            time.sleep(2)  # Allow navigation time
            self.assertEqual(self.driver.current_url, f"{url}{expected_endpoint}")

    # ✅ Test 2: Homepage Key Elements
    def test_1_homepage_elements(self):
        """Test that homepage contains key expected elements."""
        elements = [
            ("h1", "WildWareness"),
            ("p", "Platform serves"),
            ("p", "Users can"),
            (".carousel", None),  # Check if carousel exists
        ]

        for selector, expected_text in elements:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            self.assertTrue(element.is_displayed(), f"Element {selector} not found.")
            if expected_text:
                self.assertIn(expected_text, element.text)

    # ✅ Test 3: Carousel Presence
    def test_2_carousel_presence(self):
        """Check if the homepage carousel is present and visible."""
        carousel = self.driver.find_element(By.CLASS_NAME, "carousel")
        self.assertTrue(carousel.is_displayed(), "Carousel is not displayed.")

    # ✅ Test 4: Cards Exist on Model Pages
    def test_3_cards_on_pages(self):
        """Ensure each section has cards with content."""
        sections = ["incidents", "shelters", "news"]

        for section in sections:
            self.driver.get(f"{url}{section}")
            time.sleep(2)  # Allow page load
            cards = self.driver.find_elements(By.CLASS_NAME, "card")
            self.assertGreater(len(cards), 0, f"No cards found in {section} page.")

    # ✅ Test 5: "Read More" Buttons in Cards
    def test_4_read_more_buttons(self):
        """Ensure each card has a 'Read More' button."""
        sections = ["incidents", "shelters", "news"]

        for section in sections:
            self.driver.get(f"{url}{section}")
            time.sleep(2)  # Allow page load
            cards = self.driver.find_elements(By.CLASS_NAME, "card")

            for card in cards:
                button = card.find_element(By.LINK_TEXT, "Read More")
                self.assertTrue(button.is_displayed(), "Read More button missing.")

    # ✅ Test 6: About Page Team Member Cards
    def test_5_about_team_members(self):
        """Check if the About page contains 4 team member cards."""
        self.driver.get(f"{url}about")
        time.sleep(2)  # Allow page load
        team_cards = self.driver.find_elements(By.ID, "member-card")
        self.assertEqual(len(team_cards), 4, "Incorrect number of team members displayed.")

    # ✅ Test 7: Pagination Exists on Pages
    def test_6_pagination_exists(self):
        """Ensure pagination exists on data-heavy pages."""
        sections = ["incidents", "shelters", "news"]

        for section in sections:
            self.driver.get(f"{url}{section}")
            time.sleep(2)  # Allow page load
            pagination = self.driver.find_elements(By.CLASS_NAME, "pagination")
            self.assertGreater(len(pagination), 0, f"Pagination missing on {section} page.")

    # ✅ Test 8: Check Navbar Toggler (Mobile View)
    def test_7_navbar_toggler(self):
        """Ensure navbar toggler works in mobile view."""
        self.driver.set_window_size(375, 667)  # Set to mobile size

        toggler = self.driver.find_element(By.CLASS_NAME, "navbar-toggler")
        toggler.click()
        time.sleep(1)  # Allow time for toggle

        navbar = self.driver.find_element(By.ID, "navbarNav")
        self.assertTrue(navbar.is_displayed(), "Navbar did not expand after clicking toggler.")

        toggler.click()
        time.sleep(1)
        self.assertFalse(navbar.is_displayed(), "Navbar did not collapse after clicking toggler.")

    # ✅ Test 9: Check Wildfire Incident Card Details
    def test_8_wildfire_incident_card_details(self):
        """Ensure wildfire incident cards contain essential fields."""
        self.driver.get(f"{url}incidents")
        time.sleep(2)  # Allow page load

        cards = self.driver.find_elements(By.CLASS_NAME, "card")
        expected_fields = ["Name:", "County:", "Location:", "Year:", "Acres Burned:", "Status"]

        for card in cards:
            card_text = card.text
            for field in expected_fields:
                self.assertIn(field, card_text, f"Missing field '{field}' in wildfire incident card.")

    # ✅ Test 10: Check Footer Links
    def test_9_footer_links(self):
        """Verify footer contains expected links."""
        footer_links = {
            "Privacy Policy": f"{url}privacy",
            "Terms of Service": f"{url}terms",
            "Contact Us": f"{url}contact",
        }

        for link_text, expected_url in footer_links.items():
            button = self.driver.find_element(By.LINK_TEXT, link_text)
            button.click()
            time.sleep(2)  # Allow navigation time
            self.assertEqual(self.driver.current_url, expected_url)

if __name__ == "__main__":
    unittest.main()
