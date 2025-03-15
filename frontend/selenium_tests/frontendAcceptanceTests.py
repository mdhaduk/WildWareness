import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

url = "https://wildwareness.net/"

class AcceptanceTestsFrontend(unittest.TestCase):

    def setUp(self):
        # Use webdriver-manager to automatically fetch the correct ChromeDriver version
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (for CI/CD)
        chrome_options.add_argument("--no-sandbox")  # Required for running in Docker
        chrome_options.add_argument("--disable-dev-shm-usage")  # Fix resource issues
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")  # Set window size for consistent rendering
        
        # Initialize the WebDriver with automatic ChromeDriver management
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get(url)

    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()

    # Test 1: Verify correct routing in navbar
    def test_navbar_links(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(EC.url_contains("wildwareness.net"))

        nav_links = {
            "Wildfire Incidents": f"{url}incidents/",
            "Emergency Shelters": f"{url}shelters/",
            "Community Reports": f"{url}news/",
            "About": f"{url}about/"
        }

        for link_text, expected_url in nav_links.items():
            nav_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            )
            nav_link.click()
            WebDriverWait(driver, 10).until(EC.url_to_be(expected_url))
            self.assertEqual(driver.current_url, expected_url, f"Navigation to {link_text} failed")
            driver.back()

    # Test 2: Verify navbar toggle on mobile view
    def test_navbar_toggler(self):
        driver = self.driver
        driver.set_window_size(375, 667)  # Simulate mobile screen size
        toggle_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "navbar-toggler"))
        )
        toggle_button.click()
        navbar = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "navbarNav"))
        )
        self.assertTrue(navbar.is_displayed(), "Navbar should be visible after toggling")

    # Test 3: Verify carousel images load
    def test_carousel_images(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "carouselExampleAutoplaying")))
        images = driver.find_elements(By.TAG_NAME, "img")
        self.assertGreater(len(images), 0, "No images found in the carousel")

    # Test 4: Verify cards exist on each main page
    def test_cards_on_pages(self):
        driver = self.driver
        pages = ["incidents", "shelters", "news"]

        for page in pages:
            driver.get(f"{url}{page}/")
            cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
            )
            self.assertGreater(len(cards), 0, f"No cards found on {page} page")

    # Test 5: Verify pagination exists
    def test_pagination(self):
        driver = self.driver
        driver.get(f"{url}incidents/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination")))
        pagination_links = driver.find_elements(By.CSS_SELECTOR, ".pagination .page-item:not(.disabled) .page-link")
        self.assertGreater(len(pagination_links), 0, "Pagination is missing")

    # Test 6: Verify each card has a "Read More" button
    def test_read_more_buttons(self):
        driver = self.driver
        driver.get(f"{url}incidents/")
        cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
        )

        for index, card in enumerate(cards, start=1):
            try:
                read_more_button = card.find_element(By.LINK_TEXT, "Read More")
                self.assertTrue(read_more_button.is_displayed(), f"Read More button missing on card {index}")
            except Exception as e:
                self.fail(f"Card {index} is missing 'Read More' button: {str(e)}")

    # Test 7: Verify team member cards exist on the About page
    def test_about_page_members(self):
        driver = self.driver
        driver.get(f"{url}about/")
        member_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "member-card"))
        )
        self.assertGreaterEqual(len(member_cards), 4, "Expected at least 4 member cards on About page")

    # Test 8: Verify wildfire incident cards contain expected attributes
    def test_wildfire_incident_attributes(self):
        driver = self.driver
        driver.get(f"{url}incidents/")
        cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
        )
        expected_fields = ["Name:", "County:", "Location:", "Year:", "Acres Burned:", "Status"]
        
        for card in cards:
            card_text = card.text
            for field in expected_fields:
                self.assertIn(field, card_text, f"Missing expected field '{field}' in card")

    # Test 9: Verify homepage contents
    def test_homepage_contents(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(EC.url_contains("wildwareness.net"))

        title_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fire-text"))
        )
        self.assertEqual(title_text.text, "WildWareness")

        platform_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//p[strong[contains(text(), 'Platform serves')]]"))
        )
        self.assertTrue(platform_text.is_displayed(), "Platform description missing")

        users_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//p[strong[contains(text(), 'Users can')]]"))
        )
        self.assertTrue(users_text.is_displayed(), "Users description missing")

    # Test 10: Verify section titles on main pages
    def test_section_titles(self):
        driver = self.driver
        page_titles = {
            "Wildfire Incidents": f"{url}incidents/",
            "Shelters": f"{url}shelters/",
            "News Reports": f"{url}news/"
        }

        for title, expected_url in page_titles.items():
            driver.get(expected_url)
            WebDriverWait(driver, 10).until(EC.url_contains(expected_url))
            section_title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f".//h2[contains(text(), '{title}')]"))
            )
            self.assertTrue(section_title.is_displayed(), f"Section title '{title}' missing")

if __name__ == "__main__":
    unittest.main()
