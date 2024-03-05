from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to your resume file using raw string literal
resume_path = r'C:\path\to\your\resume.docx'

# Dice.com credentials
username = 'bamboowalaarbaz995@gmail.com'
password = 'Imrider99672'

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

try:
    # Navigate to the Dice login page
    driver.get("https://www.dice.com/dashboard/login")

    # Close the cookie consent popup if it appears
    try:
        cookie_popup = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')))
        cookie_popup.click()
    except:
        pass

    # Enter username and password and click login button
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email')))
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-automation-id="submitBtn"]')))

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    # Wait for the login process to complete
    WebDriverWait(driver, 10).until(EC.url_contains('dashboard'))

    # Navigate to the Dice job listing page
    driver.get("https://www.dice.com/jobs?q=data%20engineer&location=")

    # Click on the job listing
    job_listing = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.card-link'))
    )
    job_listing.click()

    # Click on the "Apply" button
    apply_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Apply")]'))
    )
    apply_button.click()

    # Fill out the application form (if any)
    resume_upload_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
    )
    resume_upload_button.send_keys(resume_path)

    # Wait for the submit button to be clickable
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Submit Application")]'))
    )

    # Click the submit button
    submit_button.click()

    print("Application submitted successfully!")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser window
    driver.quit()
