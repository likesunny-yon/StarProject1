from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import sys, os

def newInstance(email, pwd, url):
    options = webdriver.ChromeOptions()
    # options.add_extension(os.path.join(os.getcwd(), 'extensions', 'gighmmpiobklfepjocnamgkkbiglidom-5.6.0-Crx4Chrome.com.crx'))
    # options.add_argument('load-extension=' + os.path.join(os.getcwd(), 'extensions', 'XBlocker 1.0.4 - langpack'))
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://www.upwork.com/ab/account-security/login")
    sleep(1)
    driver.switch_to.window(driver.window_handles[0])

    wait = WebDriverWait(driver, 20)

    # Wait for email input field to appear and enter email
    login_username = wait.until(EC.visibility_of_element_located((By.ID, "login_username")))
    login_username.send_keys(email)

    # Click on continue button
    login_password_continue = wait.until(EC.element_to_be_clickable((By.ID, "login_password_continue")))
    login_password_continue.click()

    # Wait for password input field to appear and enter password
    login_password = wait.until(EC.visibility_of_element_located((By.ID, "login_password")))
    login_password.send_keys(pwd)

    # Click on continue button
    login_control_continue = wait.until(EC.element_to_be_clickable((By.ID, "login_control_continue")))
    login_control_continue.click()

    # sleep(3)
    # driver.get(url)
    try:
        # Continuously check if the browser window is closed
        while True:
            try:
                # Check if the browser is still open by accessing a property (e.g., title)
                _ = driver.title
                sleep(10)
            except WebDriverException:
                # Browser window is closed, break out of the loop and quit the script
                print("INFO: Browser window is closed.")
                break

    finally:
        # Quit the browser and end the script process
        driver.quit()

if __name__ == '__main__':
    email = sys.argv[1]
    pwd = 'P@ssw0rd123123'
    url = sys.argv[2]
    newInstance(email, pwd, url)