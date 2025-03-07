from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import unittest

class TestApp(unittest.TestCase):

    def setUp(self):
        # Set up Firefox WebDriver with the correct path using Service
        gecko_path = '/Users/alazartadesse/Downloads/geckodriver'  # Update this path to your actual GeckoDriver path
        service = Service(gecko_path)
        options = webdriver.FirefoxOptions()
        options.headless = True  # Run in headless mode (no GUI)
        self.driver = webdriver.Firefox(service=service, options=options)
        self.driver.get('http://127.0.0.1:5000')  # Open the home page

    def tearDown(self):
        # Quit the WebDriver after each test
        self.driver.quit()

    def test_home_page(self):
        # Navigate to the home page and check if it renders correctly
        page_title = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertEqual(page_title, 'Bookstore')

    def test_login_page(self):
        # Test if login page is rendered correctly
        self.driver.get('http://127.0.0.1:5000/login')
        page_title = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertEqual(page_title, 'Login')

    def test_search_form(self):
        # Test the search functionality using the form

        # Wait for the search input to be present
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'search'))
        )
        
        # Clear the search box (in case it's pre-filled) and type the search query
        search_box.clear()
        search_box.send_keys('To Kill a Mockingbird')  # Typing '1984' into the search field

        # Wait for the submit button to be present and click it explicitly
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
        )
        submit_button.click()  # Click the submit button

        # Wait for the results to appear (wait for a specific element that indicates the page is loaded)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))  # Assuming results appear in <h2> tags
        )

        # Check if the search results contain the term '1984'
        results = self.driver.find_elements(By.TAG_NAME, 'h2')
        search_term_found = any('To Kill a Mockingbird' in result.text for result in results)

        self.assertTrue(search_term_found, "Search results do not contain 'To Kill a Mockingbird'")

    def test_login_functionality(self):
        # Test login functionality
        self.driver.get('http://127.0.0.1:5000/login')
        
        # Wait for username and password fields to be present
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        password_field = self.driver.find_element(By.NAME, 'password')
        
        # Enter login data and submit
        username_field.send_keys('admin')
        password_field.send_keys('adminpassword')
        password_field.send_keys(Keys.RETURN)  # Simulate pressing the 'Enter' key
        
        # Wait for the admin dashboard to load (wait for an element that confirms the page has loaded)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )
        
        # Add an assertion to check the result
        page_title = self.driver.find_element(By.TAG_NAME, 'h2').text
        self.assertEqual(page_title, 'Admin Dashboard')  # Update with expected result after login

if __name__ == '__main__':
    unittest.main()
