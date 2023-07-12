from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sqlite3
import os

def ScreenShot(driver, email, pwd, flag):
    driver.get("https://www.upwork.com/ab/proposals/")
    if flag:
        sleep(1)
        driver.switch_to.window(driver.window_handles[0])
    wait = WebDriverWait(driver, 10)

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

    sleep(7)
    
    driver.save_screenshot('static/' + email + '.png')
    driver.execute_script('document.querySelector(".link-logout.nav-menu-item").click()')

def getScreenShot():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    # options.add_extension(os.path.join(os.getcwd(), 'extensions', 'gighmmpiobklfepjocnamgkkbiglidom-5.6.0-Crx4Chrome.com.crx'))
    # options.add_argument('load-extension=' + os.path.join(os.getcwd(), 'extensions', 'XBlocker 1.0.4 - langpack'))

    i = 0
    driver = False

    while 1:
        db_fullpath = os.path.join(config.DBPath, config.DBName)
        conn = sqlite3.connect(db_fullpath)
        cur = conn.cursor()
        cur.execute('SELECT email from accounts WHERE status="sent"')
        emails = cur.fetchall()
        emails = [email[0] for email in emails]
        emails = emails[::-1]
        conn.commit()
        conn.close()
        for email in emails:
            print(email)
            try:
                if email.count("@") > 0:
                    if i % 5 == 0:
                        i = 0
                        if driver: driver.quit()
                        driver = webdriver.Chrome(options=options)
                    if i == 0:
                        ScreenShot(driver, email, "P@ssw0rd123123", True)
                    else:
                        ScreenShot(driver, email, "P@ssw0rd123123", False)
                    i += 1
            except Exception as e:
                print("error:", str(e))
                continue
        break

if __name__ == '__main__':
    getScreenShot()