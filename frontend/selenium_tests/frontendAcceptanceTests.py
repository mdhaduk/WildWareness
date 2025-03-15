import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


url = "https://wildwareness.net/"
class acceptance_tests_frontend(unittest.TestCase):

    def setUp(self):
        # Enhanced setup for CI environment
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")  # Required for running in Docker
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")  # Set proper window size
        
        # Initialize the WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url)

    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()


    # Test to verify correct routing in navbar
    def test_0(self) -> None:
        driver = self.driver
        driver.get(url)
        # CHANGE THIS LINE^^^^^^^^^^^^^^^^^^^^^^^^^^
        WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")  # Ensure you are on the expected URL
        )
        # Wait for the navigation bar to load (you can also use `test_navigation_bar_exists` here)
        nav_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'navbar-nav'))  # Change the ID based on your nav bar
        )
        # Define the links you want to check in the navigation bar
        links = [
            {'name': 'Wildfire Incidents', 'url': f'{url}incidents/'},
            {'name': 'Emergency Shelters', 'url': f'{url}shelters/'},
            {'name': 'Community Reports', 'url': f'{url}news/'}, 
            {'name': 'About', 'url': f'{url}about/'}
        ]
        # Loop through each link and check its behavior
        for link in links:
            # Ensure fresh navigation bar is located in case of dynamic content or page reload
            # to prevent stale element exceptiobs
            nav_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'navbar-nav'))
             )

            # Find the link element by link text or another method
            nav_link = nav_bar.find_element(By.LINK_TEXT, link['name'])
            # Assert that the link is visible
            self.assertTrue(nav_link.is_displayed(), f"{link['name']} link is not displayed")
            # Click the link and wait for the page to load
            nav_link.click()
            WebDriverWait(driver, 10).until(
                EC.url_to_be(link['url'])  # Wait until the page URL matches
            )
            # Assert that the page URL is correct
            self.assertEqual(driver.current_url, link['url'], f"Navigation to {link['name']} failed")
            # Go back to the original page to continue testing the other links
            driver.back()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'navbar-nav'))  # Wait for the nav bar to reappear
            )

    # Test Nav-Bar Toggler
    def test_1(self) -> None:
        driver = self.driver
        driver.get(url)
        # CHANGE THIS LINE^^^^^^^^^^^^^^^^^^^^^^^^^^
        WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")  # Ensure you are on the expected URL
        )
        
        # Needs to set window size to small size or nav bar toggler doesn't show up
        driver.set_window_size(375, 667) # Set to a typical mobile screen size (e.g., iPhone 6/7/8)

        # Find the toggle button
        toggle_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "navbar-toggler"))
        )

        # Click on the toggle button to open the navbar
        toggle_button.click()

        # Wait for the menu to expand
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "navbarNav"))
        )

        # Find the navbar collapse element to check if it is visible
        navbar = driver.find_element(By.ID, "navbarNav")

        # Assert that the navbar is visible after the toggle
        assert navbar.is_displayed(), "Navbar should be displayed after toggle"

        # Optionally, you can also verify the collapsed state
        # Click on the toggle again to collapse the navbar
        toggle_button.click()

        # Wait for the menu to collapse
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "navbarNav"))
        )

        # Assert that the navbar is not visible after the second toggle
        assert not navbar.is_displayed(), "Navbar should not be visible after toggle"

    # Check image carousel and if images present on home page
    def test_2(self) -> None:
        driver = self.driver
        driver.get(url)
        # CHANGE THIS LINE^^^^^^^^^^^^^^^^^^^^^^^^^^
        WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")  # Ensure you are on the expected URL
        )
        # Wait until the page is loaded and carousel is available
        # Assuming the carousel has a class name 'carousel', adjust the selector as per your HTML
        carousel_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "carouselExampleAutoplaying"))
        )
        
        # Check if there are images inside the carousel
        images = carousel_element.find_elements(By.TAG_NAME, "img")
        
        # Assert that at least one image is present in the carousel
        self.assertGreater(len(images), 0, "No images found in the carousel.")
        
        # Optionally, verify that the images have a valid src attribute
        for image in images:
            self.assertTrue(image.get_attribute("src"), "Image source is empty.")

    # Check if there are cards on each of the model pages
    def test_3(self) -> None:
        driver = self.driver
        driver.get(url)
        WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")  # Ensure you are on the expected URL
        )
        # Define the links you want to click in the navbar
        navbar_links = {
            "Wildfire Incidents": f'{url}incidents/',
            "Emergency Shelters": f'{url}shelters/',
            "Community Reports": f'{url}news/',
        }

        for link_text, expected_url in navbar_links.items():
            # Click on the navbar link
            """Click a navbar link by link text"""
            navbar_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            )
            navbar_link.click()

            # Wait for the page to load (You can also customize wait time for page load)
            WebDriverWait(driver, 10).until(
                EC.url_contains(expected_url)  # Wait until the URL contains the expected endpoint
            )

            """Check if cards are present on the page"""
            # Wait for cards to load
            cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))  # Replace with your card class or ID
            )

            # Assert that cards are found on the page
            self.assertGreater(len(cards), 0, "No cards found on this page.")  # Make sure at least 1 card exists

            # Check if each card is visible
            for card in cards:
                self.assertTrue(card.is_displayed(), "Card is not displayed")

    def test_4(self) -> None:
        driver = self.driver
        driver.get(url)

        # Ensure the page is loaded and we are on the correct URL
        WebDriverWait(driver, 10).until(
            EC.url_contains("wildwareness.net")  # Ensure you are on the expected URL
        )

        # Define the links you want to click in the navbar
        navbar_links = {
            "Wildfire Incidents": f'{url}incidents/',
            "Emergency Shelters": f'{url}shelters/',
            "Community Reports": f'{url}news/',
        }

        for link_text, expected_url in navbar_links.items():
            # Click on the navbar link
            navbar_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            )
            navbar_link.click()

            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.url_contains(expected_url)  # Wait until the URL contains the expected endpoint
            )

            # Wait for the pagination to be present on the page
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.pagination'))
            )

            # Pagination logic
            pagination_links = driver.find_elements(By.CSS_SELECTOR, '.pagination .page-item:not(.disabled) .page-link')
            total_pages = len(pagination_links)
            self.assertTrue(total_pages > 0, "There is no pagination")

    # Check if each card has read more button
    def test_5(self) -> None:
        driver = self.driver
        driver.get(url)
        # Ensure the page is loaded and we are on the correct URL
        WebDriverWait(driver, 10).until(
            EC.url_contains("wildwareness.net")  # Ensure you are on the expected URL
        )

        # Define the links you want to click in the navbar
        navbar_links = {
            "Wildfire Incidents": f'{url}incidents/',
            "Emergency Shelters": f'{url}shelters/',
            "Community Reports": f'{url}news/',
        }

        for link_text, expected_url in navbar_links.items():
            # Click on the navbar link
            navbar_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            )
            navbar_link.click()

            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.url_contains(expected_url)
            )
            
            # Wait for cards to load
            cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
            )

            # Loop through each card and check if it has a "Read More" button
            for index, card in enumerate(cards, start=1):
                try:
                    # Try to find the "Read More" button inside the card
                    read_more_button = card.find_element(By.LINK_TEXT, "Read More")
                    
                    # If found, ensure it is visible and enabled
                    self.assertTrue(read_more_button.is_displayed(), f"Read More button in card {index} is not visible")
                    self.assertTrue(read_more_button.is_enabled(), f"Read More button in card {index} is not clickable")

                except Exception as e:
                    self.fail(f"Card {index} is missing the Read More button or there was an error: {str(e)}")

    # Check About Page Team Member Contents
    def test_6(self) -> None:
        driver = self.driver
        driver.get(url)

        # Ensure the page is loaded and we are on the correct URL
        WebDriverWait(driver, 10).until(
            EC.url_contains("wildwareness.net")
        )
        
        # Click on the navbar link
        navbar_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "About"))
        )
        navbar_link.click()

        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.url_contains(f"{url}about")
        )
        
        # Find all the member cards
        member_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, 'member-card'))
        )

        # Assert there are exactly 4 member cards
        self.assertEqual(len(member_cards), 4, f"Expected 4 member cards, but found {len(member_cards)}")

        # Loop through each member card and verify that all required elements are present
        for index, card in enumerate(member_cards, start=1):
            try:
                # Check if the image, name, bio, and responsibilities are present
                image = card.find_element(By.CSS_SELECTOR, '.member-photo')
                name = card.find_element(By.TAG_NAME, 'h4')
                bio = card.find_element(By.XPATH, ".//p[strong[contains(text(), 'Bio:')]]")
                responsibilities = card.find_element(By.XPATH, ".//p[strong[contains(text(), 'Major Responsibilities:')]]")
                stats = card.find_element(By.CSS_SELECTOR, '.member-stats')

                # Verify that all the elements are visible and have non-empty values
                self.assertTrue(image.is_displayed(), f"Image for member {index} is not displayed")
                self.assertTrue(name.is_displayed(), f"Name for member {index} is not displayed")
                self.assertTrue(bio.is_displayed(), f"Bio for member {index} is not displayed")
                self.assertTrue(responsibilities.is_displayed(), f"Responsibilities for member {index} are not displayed")
                self.assertTrue(stats.is_displayed(), f"Stats for member {index} are not displayed")

                # Optionally, you can also check if the name and bio are not empty
                self.assertGreater(len(name.text.strip()), 0, f"Name for member {index} is empty")
                self.assertGreater(len(bio.text.strip()), 0, f"Bio for member {index} is empty")
                self.assertGreater(len(responsibilities.text.strip()), 0, f"Responsibilities for member {index} are empty")

            except Exception as e:
                self.fail(f"Member {index} card failed due to error: {str(e)}")

    # Check if expected attributes are on wildfire cards
    def test_7(self) -> None:
        driver = self.driver
        # Open the URL
        driver.get(url + "incidents/")

        # Wait for the cards to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
        )

        # Get all card elements
        cards = driver.find_elements(By.CLASS_NAME, "card")

        expected = ["Name:", "County:", "Location:", "Year:", "Acres Burned:", "Status"]
        # Iterate over the cards to check for expected fields
        for index, card in enumerate(cards):       
            text = card.text
            for i in range(4):
                assert expected[i] in text

    # Check contents of Home Page
    def test_8(self) -> None:
        driver = self.driver
        driver.get(url)
 
        # Ensure the page is loaded and we are on the correct URL
        WebDriverWait(driver, 10).until(
            EC.url_contains("wildwareness.net")
        )
        
        text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fire-text"))
        )
        self.assertEqual(text.text, "WildWareness")
        
        # Check for platform serves text
        text_two = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//p[strong[contains(text(), 'Platform serves')]]"))
        )
        self.assertTrue(text_two.is_displayed(), f"Doesn't include purpose of platform")
        
        # Check users text
        text_three = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//p[strong[contains(text(), 'Users can')]]"))
        )
        self.assertTrue(text_three.is_displayed(), f"Doesn't include what users can do")
    
    def test_9(self) -> None:
        driver = self.driver
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.url_contains("wildwareness.net")
        )
        
        # Define the links you want to click in the navbar
        navbar_links = {
            "Wildfire Incidents": f'{url}incidents/',
            "Emergency Shelters": f'{url}shelters/',
            "Community Reports": f'{url}news/',
        }
        expected = ["Wildfire Incidents", "Shelters", "News Reports"]
        index = 0
        
        for link_text, expected_url in navbar_links.items():
            # Click on the navbar link
            navbar_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            )
            navbar_link.click()

            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.url_contains(expected_url)
            )
            
            # Replace sleep with explicit wait
            text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f".//h2[contains(text(), '{expected[index]}')]"))
            )
            self.assertTrue(text.is_displayed(), f'{expected[index]}')
            index += 1

if __name__ == "__main__":
    unittest.main()