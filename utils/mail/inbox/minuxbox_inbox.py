from selenium.webdriver.common.by import By

from utils.automation.selenium_tools import waitInfinite


def verifyEmail(minuteboxDriver):
    minuteboxDriver.execute_script('x = document.querySelectorAll("td.from")[0];if(x.textContent == " Upwork Notifications ") x.click()')
    sleep(5)
    iframe = minuteboxDriver.find_element(By.ID, "iframeMail")
    minuteboxDriver.switch_to.frame(iframe)

def wait_upwork_email(minuteboxDriver):
    if (not minuteboxDriver):
        print("Unformatted browser driver. At first init this object.")
        return ''
    waitInfinite(lambda: verifyEmail(minuteboxDriver))
    verify_url = minuteboxDriver.find_elements(By.TAG_NAME, 'a')[1].get_attribute('href')
    
    try:
        minuteboxDriver.quit()
    except:
        try:
            minuteboxDriver.close()
        except:
            pass
    return verify_url