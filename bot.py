import ssl
import certifi
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
import undetected_chromedriver as uc  # Anti-detection
from unidecode import unidecode

# Fix SSL verification
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = ssl._create_unverified_context

# Chrome options
chrome_options = ChromeOptions()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Use undetected_chromedriver to avoid detection
driver = uc.Chrome(options=chrome_options)

# Data preparation function
def generate_account_details():
    french_first_names = ["Amélie", "Antoine", "Aurélie", "Benoît", "Camille", "Charles", "Chloé", "Claire", "Clément"]
    french_last_names = ["Leroy", "Moreau", "Bernard", "Dubois", "Durand", "Lefebvre", "Mercier", "Dupont"]
    first_name = random.choice(french_first_names)
    last_name = random.choice(french_last_names)
    username = f"{unidecode(first_name).lower()}.{unidecode(last_name).lower()}{random.randint(1000, 9999)}"
    password = f"{random.choice(['P@ssw0rd', 'x0z!Tricky', '1AbcD%'])}{random.randint(1000, 9999)}"
    birthday = {"day": str(random.randint(1, 28)), "month": str(random.randint(1, 12)), "year": str(random.randint(1985, 2003))}
    gender = random.choice(["1", "2", "3"])  # 1: Female, 2: Male, 3: Not specified
    return first_name, last_name, username, password, birthday, gender

# Generate account details
first_name, last_name, username, password, birthday, gender = generate_account_details()

# Fill the account creation form
def fill_form(driver):
    try:
        print("Navigating to the sign-up page.")
        driver.get("https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp")
        wait = WebDriverWait(driver, 20)

        # Page 1: First and last name
        wait.until(EC.visibility_of_element_located((By.NAME, "firstName"))).send_keys(first_name)
        wait.until(EC.visibility_of_element_located((By.NAME, "lastName"))).send_keys(last_name)

        # Scroll into view if necessary and click next button using JavaScript
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='LgbsSe']")))
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)

        # Page 2: Birthday and gender
        Select(wait.until(EC.presence_of_element_located((By.ID, "month")))).select_by_value(birthday['month'])
        wait.until(EC.presence_of_element_located((By.ID, "day"))).send_keys(birthday['day'])
        wait.until(EC.presence_of_element_located((By.ID, "year"))).send_keys(birthday['year'])
        Select(wait.until(EC.presence_of_element_located((By.ID, "gender")))).select_by_value(gender)

        # Scroll and click next button
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='LgbsSe']")))
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)

        # Page 3: Username
        wait.until(EC.visibility_of_element_located((By.NAME, "Username"))).send_keys(username)
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='LgbsSe']")))
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)

        # Page 4: Password
        wait.until(EC.visibility_of_element_located((By.NAME, "Passwd"))).send_keys(password)
        wait.until(EC.visibility_of_element_located((By.NAME, "ConfirmPasswd"))).send_keys(password)

        # Scroll and click next button
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='LgbsSe']")))
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)

        # Page 5: Recovery email
        wait.until(EC.visibility_of_element_located((By.NAME, "recoveryEmail"))).send_keys(f"{first_name}.{last_name}@example.com")
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='LgbsSe']")))
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)

        # Page 6: Skip (no fields)
        skip_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='LgbsSe']")))
        driver.execute_script("arguments[0].scrollIntoView();", skip_button)
        driver.execute_script("arguments[0].click();", skip_button)

        # Page 7: Agree to terms
        agree_button = wait.until(EC.element_to_be_clickable((By.ID, "termsofserviceNext")))
        driver.execute_script("arguments[0].scrollIntoView();", agree_button)
        driver.execute_script("arguments[0].click();", agree_button)

        # Final confirmation
        print(f"Account created: {username}@gmail.com | Password: {password}")
    
    except Exception as e:
        print(f"Error occurred during form filling: {e}")

    # Ensure browser stays open for debugging
    input("Press Enter to close the browser...")

    driver.quit()

# Run the function
fill_form(driver)
