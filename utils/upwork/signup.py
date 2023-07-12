from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
from time import sleep
import time
import datetime
import os

from utils.automation.selenium_tools import waitInfinite
from utils.automation.selenium_tools import selectDateDropDown
from utils.automation.selenium_tools import waitUntil
from utils.automation.selenium_tools import clickByMouse
from utils.automation.selenium_tools import selectDropDown
from utils.automation.selenium_tools import inputTextObject
from utils.automation.selenium_tools import getState

import config

def createAccount(driver, profile, tempemail):
    try:
        driver.get("https://www.upwork.com/nx/signup/?dest=home")
        # sleep(1)
        # driver.switch_to.window(driver.window_handles[0])
        driver.find_element(By.ID, "button-box-4").click()
        driver.find_element(By.CSS_SELECTOR, "button[data-qa='btn-apply']").click()

        driver.find_element(By.ID, "first-name-input").send_keys(profile['first_name'])
        driver.find_element(By.ID, "last-name-input").send_keys(profile['last_name'])
        driver.find_element(By.ID, "redesigned-input-email").send_keys(tempemail)
        driver.find_element(By.ID, "password-input").send_keys("P@ssw0rd123123")

        # onetrust-accept-btn-handler
        waitInfinite(lambda: driver.find_element(By.ID, "onetrust-close-btn-container").click(), driver)

        # Validating inputed email address
        wait = WebDriverWait(driver, 10)
        action = webdriver.ActionChains(driver)
        action = webdriver.common.action_chains.ActionChains(driver)

        driver.execute_script(f'document.querySelector("#dropdown-label-7").click()')
        waitInfinite(lambda: selectDropDown(driver, "li.up-menu-item", profile['country']), driver)
        sleep(1)
        driver.execute_script('document.querySelectorAll("span.up-checkbox-replacement-helper")[0].click()')
        driver.execute_script('document.querySelectorAll("span.up-checkbox-replacement-helper")[1].click()')
        driver.execute_script('document.getElementById("button-submit-form").click()')
    except Exception as e:
        print("ERROR: Error in create account!\n", e)
        raise

    sleep(10) # Should set this value >=10, because upwork can stop your bot.
    return True

def chooseHistory(driver):
    try:
        # Are your Expert, GET_EXPERIENCE, ...
        sleep(5)
        waitInfinite(lambda: driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary").click()'), driver)

        sleep(2)
        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "input[value=\"FREELANCED_BEFORE\"]").click(), driver)
        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)

        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "input[value=\"GET_EXPERIENCE\"]").click(), driver)
        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)

        waitInfinite(lambda: driver.execute_script("x=document.querySelectorAll('input[class=\"air3-btn-box-input\"]').length - 2;document.querySelectorAll('input[class=\"air3-btn-box-input\"]')[x].click()"), driver)
        waitInfinite(lambda: driver.execute_script("x = document.querySelector('span[data-test=\"checkbox-input\"]'); console.log(x); x.click()"), driver)
        # waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "span[data-test=\"checkbox-input\"]").click(), driver)
        waitInfinite(lambda: driver.execute_script("document.querySelector('button[data-test=\"next-button\"]').click()"), driver)
    except Exception as e:
        print("ERROR: Error in choose your history!\n", e)
        raise
    return True

def selectFillMethod(driver, profile_doc):
    try:
        if (profile_doc):
            print(f"INFO: Path of profile document is : {profile_doc}\n Trying with this file.")
            waitInfinite(lambda: driver.execute_script('x=document.querySelectorAll("button.mb-3.air3-btn.air3-btn-secondary").length;document.querySelectorAll("button.mb-3.air3-btn.air3-btn-secondary")[x-3].click()'), driver)
            waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(os.path.join(os.getcwd(), profile_doc)), driver)
            sleep(10)
            waitInfinite(lambda: driver.execute_script('document.querySelector("button.air3-btn.air3-btn-primary.mb-0").click()'), driver)
        else:
            waitInfinite(lambda: driver.execute_script('x=document.querySelectorAll("button.mb-3.air3-btn.air3-btn-secondary").length;document.querySelectorAll("button.mb-3.air3-btn.air3-btn-secondary")[x-1].click()'), driver)
    except Exception as e:
        print("ERROR: Error in select fill method!\n", e)
        raise
    return True

def fillProfessional(driver, professional):
    try:
        sleep(2)
        driver.execute_script(f'document.querySelector("input.air3-input.form-control").value = "";')
        # driver.execute_script(f'document.querySelector("input.air3-input.form-control").value = "{professional}";')
        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "input.air3-input.form-control").send_keys(professional), driver)
        sleep(1)
        print("INFO: Filled professional successfully.")
    except Exception as e:
        print("ERROR: Error in fill professional!\n", e)
        raise
    return True

def fillWorkExperience(driver, experiences):
    try:
        for experience in experiences:
            expFlag = True
            if expFlag:
                waitInfinite(lambda: driver.execute_script('document.querySelectorAll("button.air3-btn.air3-btn-circle")[0].click()'), driver)
            else:
                waitInfinite(lambda: driver.execute_script('document.querySelector("button.air3-btn.air3-btn-secondary.air3-btn-circle").click()'), driver)

            if expFlag: waitInfinite(lambda: driver.find_elements(By.CSS_SELECTOR, 'input[aria-labelledby="title-label"]')[1].send_keys(""), driver)
            waitInfinite(lambda: driver.find_elements(By.CSS_SELECTOR, 'input[aria-labelledby="title-label"]')[1].send_keys(experience['role']), driver)
            waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="company-label"]').send_keys(experience['company']), driver)
            # waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="location-label"]').send_keys(city), driver)
            # waitInfinite(lambda: selectDateDropDown("location-label", "span.air3-menu-item-text", country), driver)

            sleep(0.5)

            CURRENTYEAR = datetime.now().year
            start_year = eval(experience['start'].split('.')[0])
            start_month = eval(experience['start'].split('.')[1])
            waitInfinite(lambda: selectDateDropDown("start-date-month", "span.air3-menu-item-text", start_month - 1), driver)
            waitInfinite(lambda: selectDateDropDown("start-date-year", "span.air3-menu-item-text", CURRENTYEAR - start_year), driver)

            # waitInfinite(lambda: driver.find_element(By.TAG_NAME,'textarea').send_keys(description), driver)
            # sleep(3)
            for text in experience['description']:
                waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'textarea[aria-labelledby="description-label"]').send_keys("• " + text + "\n"), driver)

            if  experience['end'] == 'current':
                driver.execute_script('document.querySelector(\'[data-qa="currently-working"]\').querySelector("label").click()')
            else:
                end_year = eval(experience['end'].split('.')[0])
                end_month = eval(experience['end'].split('.')[1])
                waitInfinite(lambda: selectDateDropDown("end-date-month", "span.air3-menu-item-text", end_month - 1), driver)
                waitInfinite(lambda: selectDateDropDown("end-date-year", "span.air3-menu-item-text", CURRENTYEAR - end_year), driver)
            driver.execute_script('document.querySelector(\'button[data-qa="btn-save"]\').click()')
        print("INFO: Filled a work experience successfully.")

    except Exception as e:
        print("ERROR: Error in fill experience!\n", e)
        raise
    return True

def fillEducation(driver, educations):
    try:
        for education in educations:
            start = eval(education['start'])
            end = eval(education['end'])

            expFlag = True
            if expFlag:
                waitInfinite(lambda: driver.execute_script('document.querySelectorAll("button.air3-btn.air3-btn-circle")[7].click()'), driver)
            else:
                waitInfinite(lambda: driver.execute_script('document.querySelector("button.air3-btn.air3-btn-secondary.air3-btn-circle").click()'), driver)

            sleep(2)
            waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="school-label"]').click(), driver)
            sleep(2)
            waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="school-label"]').send_keys(education['university']), driver)
            sleep(2)
            driver.find_element(By.CLASS_NAME, "air3-menu-item-text").click()
            sleep(1)
            waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="degree-label"]').click(), driver)
            sleep(2)
            waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="degree-label"]').send_keys(education['degree']), driver)
            sleep(3)

            action.move_to_element_with_offset(driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="degree-label"]'),50,70)
            action.click()
            sleep(1)
            action.perform()
            sleep(1)
            # debug()
            # driver.find_element(By.CLASS_NAME, "is-focused").click()
            # driver.find_element(By.CLASS_NAME, "air3-menu-item-text").click()

            waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="area-of-study-label"]').click(), driver)
            sleep(0.5)
            waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="area-of-study-label"]').send_keys(education['field']), driver)
            sleep(1)
            action.move_to_element_with_offset(driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="area-of-study-label"]'),50,70)
            action.click()
            action.perform()
            
            CURRENTYEAR = datetime.now().year
            waitInfinite(lambda: selectDateDropDown("dates-attended-label##0", "span.air3-menu-item-text", CURRENTYEAR - start + 1+5), driver)
            waitInfinite(lambda: selectDateDropDown("dates-attended-label##1", "span.air3-menu-item-text", 2030 - end + 1+5), driver)
            sleep(3)
            driver.execute_script('document.querySelector(\'button[data-qa="btn-save"]\').click()')
        print("INFO: Filled a education successfully.")

    except Exception as e:
        print("ERROR: Error in fill education!\n", e)
        raise
    return True

def fillCertification(driver, certifications):
    try:
        if len(certifications) == 0:
            return False
        else:
            pass
    except Exception as e:
        print("ERROR: Error in fill certification!\n", e)
        raise
    return True

def fillLanguage(driver, languages):
    try:
        waitInfinite(lambda: selectDateDropDown("dropdown-label-english", "span.air3-menu-item-text", 2), driver)
        count = 0
        for languageinfo in languages:
            if languageinfo["language"] == 'English': continue
            pro = eval(languageinfo['pro'])
            driver.execute_script('document.querySelector("button.air3-btn.air3-btn-secondary.air3-btn-sm").click()')
            
            waitInfinite(lambda: selectDateDropDown(f"dropdown-label-language-{count}", "span.air3-menu-item-text", languageinfo['language']), driver)
            waitInfinite(lambda: selectDateDropDown(f"dropdown-label-proficiency-{count}", "span.air3-menu-item-text", pro), driver)
            count += 1
        print("INFO: Filled language successfully.")
    except Exception as e:
        print("ERROR: Error in fill language!\n", e)
        raise
    return True

def fillSkills(driver, skills):
    try:
        # inp = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="skills-input"]')
        sleep(2)
        field = "skills-input"
        for skill in skills:
            inputTextObject(driver, skill, field)
        print("INFO: Filled skills successfully.")
    except Exception as e:
        print("ERROR: Error in fill skills!\n", e)
        raise
    return True

def fillOverview(driver, overview):
    try:
        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'textarea[aria-labelledby="overview-label"]').send_keys(profile['overview']), driver)
        print("INFO: Filled overview successfully.")
    except Exception as e:
        print("ERROR: Error in fill Overview!\n", e)
        raise
    return True

def fillServices(driver, services):
    try:
        waitUntil(lambda x: x.click(), driver, 'div[data-test="dropdown-toggle"]')
        sleep(1)

        for service in services:
            driver.execute_script(f'''
                // document.querySelectorAll(\'div[data-test="dropdown-toggle"]\')[3].click()
                var services = document.querySelectorAll('span.air3-menu-checkbox-labels');
                var toselect;
                for (let i = 0; i < services.length; i++) {{
                    console.log(services[i], '{service}');
                    if (services[i].textContent.indexOf('{service}') >= 0) {{
                        toselect = services[i].parentNode.parentNode;
                        break;
                    }}
                }}
                if (toselect) {{
                    if (toselect.getAttribute("aria-selected") == 'false') {{
                        toselect.parentNode.parentNode.parentNode.click();
                        setTimeout(() => toselect.click(), 300);
                    }}
                }}
            ''')
            sleep(0.1)
        print("INFO: Filled Services successfully.")
    except Exception as e:
        print("ERROR: Error in fill services!\n", e)
        raise
    return True

def fillRate(driver, rate):
    try:
        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[data-test="currency-input"]').clear(), driver)
        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[data-test="currency-input"]').send_keys(str(rate)), driver)
        print("INFO: Filled rate successfully.")
    except Exception as e:
        print("ERROR: Error in fill rate!\n", e)
        raise
    return True

def fillLastInfo(driver, country, street, city, zipcode, phone, photo):
    try:
        # selectDateDropDown(driver, "country-label", "span.air3-menu-item-text", country)
        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="street-label"]').send_keys(street), driver)

        field = "city-label"
        inputTextObject(driver, city, field)

        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="postal-code-label"]').send_keys(zipcode), driver)
        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby^="dropdown-label-phone-number"]').send_keys(phone), driver)
        # waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby^="state-label"]').send_keys(state), driver)
        sleep(1)
        waitInfinite(lambda: driver.execute_script("document.querySelector('button[data-qa=\"open-loader\"]').click()"), driver)
        sleep(1)

        waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(os.path.join(os.getcwd(), config.Profile_Path, photo)), driver)
        waitInfinite(lambda: driver.execute_script("document.querySelectorAll('button.air3-btn.air3-btn-primary')[5].click()"), driver)
    except Exception as e:
        print("ERROR: Error in fill last infomation!\n", e)
        raise
    return True

def signup(profile, tempEmailObject, profile_doc=False):
    start_time = time.time()
    options = webdriver.ChromeOptions()
    if config.Install_Extensions:
        options.add_extension(os.path.join(os.getcwd(), 'extensions', 'gighmmpiobklfepjocnamgkkbiglidom-5.6.0-Crx4Chrome.com.crx'))
        options.add_argument('load-extension=' + os.path.join(os.getcwd(), 'extensions', 'XBlocker 1.0.4 - langpack'))
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # Create your account
    createAccount(driver, profile, tempEmailObject.get_temp_email())

    # Verify with temp email
    driver.get(tempEmailObject.getVerifyURL())
    
    chooseHistory(driver)

    selectFillMethod(driver, profile_doc)
    # waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)

    fillProfessional(driver, profile['professional'])
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)
    print("INFO: Pass professional.")
    
    if (not profile_doc): fillWorkExperience(driver, profile['workXP'])
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)
    print("INFO: Pass work experience.")
    
    if (not profile_doc): fillEducation(driver, profile['education'])
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)
    print("INFO: Pass education.")
    
    if getState(driver).split('/')[1] == "11":
        print("INFO: Asked to fill certification.")
        if (not 'certifications' in profile):
            profile['certifications'] = []
        certifications = profile['certifications']
        if (len(certifications)):
            if (not profile_doc): fillCertification(driver, [])
            waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)
        else:
            print("INFO: Try to skip fill certification.")
            waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"skip-button\"]").click(), driver)
    print("INFO: Pass certification.")

    if (not profile_doc): fillLanguage(driver, profile['languages'])
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)
    print("INFO: Pass language.")
    
    fillSkills(driver, profile['skills'])
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)
    print("INFO: Pass skill.")
    
    if (not profile_doc): fillOverview(driver, profile['overview'])
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)
    print("INFO: Pass overview.")
    # clickByMouse(driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]"), driver)
    
    fillServices(driver, profile['services'])
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)
    print("INFO: Pass service.")
    
    fillRate(driver, profile['hourRate'])
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)
    print("INFO: Pass rate.")
    
    fillLastInfo(driver, profile['location'], profile['street'], profile['city'], profile['zipcode'], profile['phone'], profile['avatar'])
    waitInfinite(lambda: driver.find_element(By.CSS_SELECTOR, "button[data-test=\"next-button\"]").click(), driver)
    print("INFO: Pass last infomation.")

    waitInfinite(lambda: driver.execute_script('document.querySelector("button.air3-btn.width-md.m-0.air3-btn-primary").click()'), driver)
    sleep(3)
    driver.quit()
    end_time = time.time()
    execution_time = end_time - start_time
    formatted_time = time.strftime("%H:%M:%S", time.gmtime(execution_time))
    print("INFO: Pass all and quit.")
    print(f"INFO: Execution time: {formatted_time}.")
    return True
