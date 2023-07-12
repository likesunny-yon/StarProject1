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
from datetime import datetime
import sys
import os
import json

def waitInfinite(callback, driver, debug = False):
    yet = True
    while yet:
        sleep(1)
        try:
            callback()
            yet = False
        except NoSuchElementException as e:
            print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
            sleep(0.5)
            pass
        except JavascriptException as e:
            print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
            sleep(0.5)
            pass
        except StaleElementReferenceException as e:
            print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
            sleep(0.5)
            pass
        except ElementClickInterceptedException as e:
            print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
            sleep(0.5)
            pass
        except ElementNotInteractableException as e:
            print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
            sleep(0.5)
            pass
        except Exception as e:
            print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
            # sleep(0.5)
            # pass
            driver.quit()
            exit()
    sleep(2)
    return True
            
def waitUntil(callback, driver, selector):
    sleep(1)
    yet = True
    while yet:
        try:
            callback(driver.execute_script("x=document.querySelectorAll('{}').length;return document.querySelectorAll('{}')[x-1]".format(selector, selector)))
            yet = False
        except Exception as e:
            print(str(e).split('\n')[0])
            sleep(0.1)
            pass

def waitUntil_2(callback, driver, selector):
    sleep(1)
    yet = True
    while yet:
        try:
            callback(driver.find_elements(By.CSS_SELECTOR, selector)[3])
            yet = False
        except Exception as e:
            print(str(e).split('\n')[0])
            sleep(0.1)
            pass

def clickByMouse(driver, element):
    ActionChains(driver).click(element).perform()

def selectDropDown(driver, itemSelector, country):
    nations = driver.find_elements(By.CSS_SELECTOR, itemSelector)

    if str(type(country)) == "<class 'int'>":
        driver.execute_script(f'document.querySelectorAll("{itemSelector}")[{str(country)}].click()')
    else:
        for i in range(len(nations)):
            try:
                if nations[i].text.find(country) >= 0:
                    driver.execute_script(f'document.querySelectorAll("{itemSelector}")[{str(i)}].click()')
                    break
            except:
                pass

def selectDateDropDown(driver, dropdownId, itemSelector, country):
    tmp = dropdownId.split('##')
    if len(tmp) == 2:
        dropdownId = tmp[0]
        driver.execute_script(f'document.querySelectorAll(\'div[aria-labelledby^="{dropdownId}"]\')[{tmp[1]}].click()')
    else:
        driver.execute_script(f'document.querySelector(\'div[aria-labelledby^="{dropdownId}"]\').click()')
    sleep(2)
    nations = driver.find_elements(By.CSS_SELECTOR, itemSelector)

    if str(type(country)) == "<class 'int'>":
        driver.execute_script(f'document.querySelectorAll("{itemSelector}")[{str(country)}].click()')
    else:
        for i in range(len(nations)):
            try:
                if nations[i].text.find(country) >= 0:
                    driver.execute_script(f'document.querySelectorAll("{itemSelector}")[{str(i)}].click()')
                    break
            except:
                pass

def inputTextObject(driver, item, field):
    # field = "skills-input"
    waitUntil(lambda x: x.click(), driver, f'input[aria-labelledby="{field}"]')
    sleep(1)
    inp = driver.find_element(By.CSS_SELECTOR, f'input[aria-labelledby="{field}"]')
    for i in item:
        inp.send_keys(i)
    sleep(0.5)
    flag = True
    while flag:
        nations = driver.find_elements(By.CSS_SELECTOR, "span.air3-menu-item-text")
        flag = len(nations) == 0

    for i in range(len(nations)):
        try:
            if item.lower() in nations[i].text.lower():
                # driver.execute_script(f'document.querySelectorAll("span.air3-menu-item-text")[{str(i)}].click()')
                nations[i].click()
                break
        except:
            pass
    waitUntil(lambda x: x.clear(), driver, f'input[aria-labelledby="{field}"]')
    return True

def getState(driver):
    statespan = driver.find_element(By.CSS_SELECTOR, 'span.text-base-sm')
    # print("===================")
    # print(statespan.text)
    if statespan:
        return statespan.text
    return False
