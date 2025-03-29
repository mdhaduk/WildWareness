import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

url = "https://wildwareness.net/"

@pytest.fixture
def driver():
    # Set up for the webdriver with headless options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")  # Required for running in Docker
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")  # Set proper window size

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

# Test to verify correct routing in navbar
def test_0(driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")
    )
    
    nav_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'navbar-nav'))
    )
    
    links = [
        {'name': 'Wildfire Incidents', 'url': f'{url}incidents/'},
        {'name': 'Emergency Shelters', 'url': f'{url}shelters/'},
        {'name': 'Community Reports', 'url': f'{url}news/'}, 
        {'name': 'About', 'url': f'{url}about/'}
    ]
    
    for link in links:
        nav_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'navbar-nav'))
        )
        nav_link = nav_bar.find_element(By.LINK_TEXT, link['name'])
        assert nav_link.is_displayed(), f"{link['name']} link is not displayed"
        nav_link.click()
        WebDriverWait(driver, 10).until(
            EC.url_to_be(link['url'])
        )
        assert driver.current_url == link['url'], f"Navigation to {link['name']} failed"
        driver.back()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'navbar-nav'))
        )

# Test Nav-Bar Toggler
def test_1(driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")
    )
    driver.set_window_size(375, 667)

    toggle_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "navbar-toggler"))
    )
    toggle_button.click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "navbarNav"))
    )

    navbar = driver.find_element(By.ID, "navbarNav")
    assert navbar.is_displayed(), "Navbar should be displayed after toggle"

# Check image carousel and if images are present on the home page
def test_2(driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")
    )

    carousel_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "carouselExampleAutoplaying"))
    )

    images = carousel_element.find_elements(By.TAG_NAME, "img")
    assert len(images) > 0, "No images found in the carousel."
    for image in images:
        assert image.get_attribute("src"), "Image source is empty."

# Check if there are cards on each of the model pages
def test_3(driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")
    )

    navbar_links = {
        "Wildfire Incidents": f'{url}incidents/',
        "Emergency Shelters": f'{url}shelters/',
        "Community Reports": f'{url}news/',
    }

    for link_text, expected_url in navbar_links.items():
        navbar_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, link_text))
        )
        navbar_link.click()
        WebDriverWait(driver, 10).until(
            EC.url_contains(expected_url)
        )
        
        cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
        )

        assert len(cards) > 0, "No cards found on this page."
        for card in cards:
            assert card.is_displayed(), "Card is not displayed"

def test_4(driver):
    driver.get(url)
    # Ensure the page is loaded and we are on the correct URL
    WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")
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

        # Wait for the pagination to be present on the page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.pagination'))
        )

        # Pagination logic
        pagination_links = driver.find_elements(By.CSS_SELECTOR, '.pagination .page-item:not(.disabled) .page-link')
        total_pages = len(pagination_links)
        assert total_pages > 0, "There is no pagination"

# Check if each card has "Read More" button
def test_5(driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")
    )

    navbar_links = {
        "Wildfire Incidents": f'{url}incidents/',
        "Emergency Shelters": f'{url}shelters/',
        "Community Reports": f'{url}news/',
    }

    for link_text, expected_url in navbar_links.items():
        navbar_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, link_text))
        )
        navbar_link.click()
        WebDriverWait(driver, 10).until(
            EC.url_contains(expected_url)
        )

        cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
        )

        for index, card in enumerate(cards, start=1):
            try:
                read_more_button = card.find_element(By.LINK_TEXT, "Read More")
                assert read_more_button.is_displayed(), f"Read More button in card {index} is not visible"
                assert read_more_button.is_enabled(), f"Read More button in card {index} is not clickable"
            except Exception as e:
                pytest.fail(f"Card {index} is missing the Read More button or there was an error: {str(e)}")

# Check About Page Team Member Contents
def test_6(driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")
    )

    navbar_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "About"))
    )
    navbar_link.click()
    WebDriverWait(driver, 10).until(
        EC.url_contains(f"{url}about")
    )

    member_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'member-card'))
    )

    assert len(member_cards) == 4, f"Expected 4 member cards, but found {len(member_cards)}"

    for index, card in enumerate(member_cards, start=1):
        try:
            image = card.find_element(By.CSS_SELECTOR, '.member-photo')
            name = card.find_element(By.TAG_NAME, 'h4')
            bio = card.find_element(By.XPATH, ".//p[strong[contains(text(), 'Bio:')]]")
            responsibilities = card.find_element(By.XPATH, ".//p[strong[contains(text(), 'Major Responsibilities:')]]")
            stats = card.find_element(By.CSS_SELECTOR, '.member-stats')

            assert image.is_displayed(), f"Image for member {index} is not displayed"
            assert name.is_displayed(), f"Name for member {index} is not displayed"
            assert bio.is_displayed(), f"Bio for member {index} is not displayed"
            assert responsibilities.is_displayed(), f"Responsibilities for member {index} are not displayed"
            assert stats.is_displayed(), f"Stats for member {index} are not displayed"

            assert len(name.text.strip()) > 0, f"Name for member {index} is empty"
            assert len(bio.text.strip()) > 0, f"Bio for member {index} is empty"
            assert len(responsibilities.text.strip()) > 0, f"Responsibilities for member {index} are empty"

        except Exception as e:
            pytest.fail(f"Member {index} card failed due to error: {str(e)}")

# Check if expected attributes are on wildfire cards
def test_7(driver):
    driver.get(url + "incidents/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
    )

    cards = driver.find_elements(By.CLASS_NAME, "card")
    expected = ["Name:", "County:", "Location:", "Year:", "Acres Burned:", "Status"]
    
    for index, card in enumerate(cards):
        text = card.text
        for i in range(4):
            assert expected[i] in text

# Check contents of Home Page
def test_8(driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")
    )

    text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fire-text"))
    )
    assert text.text == "WildWareness"

    text_two = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, ".//p[strong[contains(text(), 'Platform serves')]]"))
    )
    assert text_two.is_displayed(), "Doesn't include purpose of platform"
    
    text_three = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, ".//p[strong[contains(text(), 'Users can')]]"))
    )
    assert text_three.is_displayed(), "Doesn't include what users can do"

# Test Navbar Links
def test_9(driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.url_contains("wildwareness.net")
    )

    navbar_links = {
        "Wildfire Incidents": f'{url}incidents/',
        "Emergency Shelters": f'{url}shelters/',
        "Community Reports": f'{url}news/',
    }
    expected = ["Wildfire Incidents", "Shelters", "News Reports"]
    
    index = 0
    for link_text, expected_url in navbar_links.items():
        navbar_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, link_text))
        )
        navbar_link.click()
        WebDriverWait(driver, 10).until(
            EC.url_contains(expected_url)
        )
        
        text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f".//h2[contains(text(), '{expected[index]}')]"))
        )
        assert text.is_displayed(), f'{expected[index]}'
        index += 1
