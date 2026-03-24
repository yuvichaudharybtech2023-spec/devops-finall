import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Get the absolute path of the local HTML file
HTML_FILE_PATH = "file:///" + os.path.abspath("index.html").replace('\\', '/')

@pytest.fixture(scope="module")
def driver():
    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Run headless if required by Jenkins later
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture(autouse=True)
def load_page(driver):
    # Load the page before each test
    driver.get(HTML_FILE_PATH)
    time.sleep(1) # Wait briefly for rendering

# 1. Check whether the form page opens successfully
def test_page_loads_successfully(driver):
    assert "Student Feedback Registration Form" in driver.title
    assert driver.find_element(By.TAG_NAME, "h2").text == "Student Feedback Form"

# 2. Leave mandatory fields blank and check error messages
def test_mandatory_fields_blank(driver):
    driver.find_element(By.ID, "submitBtn").click()
    
    assert "Student Name is required" in driver.find_element(By.ID, "nameError").text
    assert "Email ID is required" in driver.find_element(By.ID, "emailError").text
    assert "Mobile Number is required" in driver.find_element(By.ID, "mobileError").text
    assert "Please select a department" in driver.find_element(By.ID, "departmentError").text
    assert "Please select your gender" in driver.find_element(By.ID, "genderError").text
    assert "Feedback comments cannot be blank" in driver.find_element(By.ID, "commentsError").text

# 3. Enter invalid email format and verify validation
def test_invalid_email_format(driver):
    driver.find_element(By.ID, "email").send_keys("invalidemail")
    driver.find_element(By.ID, "submitBtn").click()
    assert "valid email format" in driver.find_element(By.ID, "emailError").text

# 4. Enter invalid mobile number and verify validation
def test_invalid_mobile_number(driver):
    # Less than 10 digits
    mobile_input = driver.find_element(By.ID, "mobile")
    mobile_input.send_keys("12345")
    driver.find_element(By.ID, "submitBtn").click()
    assert "exactly 10 valid digits" in driver.find_element(By.ID, "mobileError").text

    # Clear and enter alphabets
    mobile_input.clear()
    mobile_input.send_keys("abcdefghij")
    driver.find_element(By.ID, "submitBtn").click()
    assert "exactly 10 valid digits" in driver.find_element(By.ID, "mobileError").text

# 5. Check whether dropdown selection works properly
def test_dropdown_selection(driver):
    dept_select = Select(driver.find_element(By.ID, "department"))
    dept_select.select_by_value("Computer Science")
    assert dept_select.first_selected_option.text == "Computer Science"

# 6. Check whether buttons such as Submit and Reset work correctly
def test_reset_button_functionality(driver):
    # Fill in some data
    driver.find_element(By.ID, "studentName").send_keys("John Doe")
    driver.find_element(By.ID, "email").send_keys("john@example.com")
    
    # Click reset
    driver.find_element(By.ID, "resetBtn").click()
    
    # Verify fields are cleared
    assert driver.find_element(By.ID, "studentName").get_attribute("value") == ""
    assert driver.find_element(By.ID, "email").get_attribute("value") == ""

# 7. Enter valid data and verify successful submission
def test_valid_submission(driver):
    driver.find_element(By.ID, "studentName").send_keys("John Doe")
    driver.find_element(By.ID, "email").send_keys("john.doe@example.college.edu")
    driver.find_element(By.ID, "mobile").send_keys("9876543210")
    
    dept_select = Select(driver.find_element(By.ID, "department"))
    dept_select.select_by_value("Electrical Engineering")
    
    driver.find_element(By.ID, "genderMale").click()
    
    # Needs to be at least 10 words
    long_feedback = "The course structure is great, but I think we need more practical labs."
    driver.find_element(By.ID, "comments").send_keys(long_feedback)
    
    driver.find_element(By.ID, "submitBtn").click()
    
    success_msg = driver.find_element(By.ID, "successMessage")
    assert success_msg.is_displayed()
    assert "Successfully submitted" in success_msg.text
