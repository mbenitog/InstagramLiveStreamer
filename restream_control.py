import os
import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def create_chrome_driver(headless):
    chromedriver_path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))), 'chromedriver')

    chrome_home_dir = sys.argv[0][:sys.argv[0].rfind("/")] + '/chrome_data'

    o = Options()
    if headless:
        o.add_argument("--headless")
        o.add_argument("--no-sandbox")
        o.add_argument("--window-size=1280,720")
    o.add_argument("--user-data-dir=" + chrome_home_dir)	
    driver = webdriver.Chrome(chromedriver_path, options=o)
    driver.implicitly_wait(1)
    return driver


def manual_login(url):						# Usually the first thing to do so the next page loads are already logged in
    driver = create_chrome_driver(False)    # Headless mode off for manual login
    driver.get(url)
    try:
        WebDriverWait(driver, 300).until(
          EC.presence_of_element_located((By.ID, "jsChannelList"))
        )
        driver.close()
        return 1
    except:
        driver.close()
        return -1


def change_key(newKey, m_login):
    reio_url = "https://restream.io/channel"

    if m_login:
        return manual_login(reio_url)

    driver = create_chrome_driver(True)     # Create driver in headless mode?
    driver.get(reio_url)

    # Click settings button
    try:
        # check page (main page of restream.io) with ID "jsChannelList" is loaded
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "jsChannelList"))
        )
    except:
        driver.close()
        return -2  # Error, could not load restream page
    finally:
        # click link of settings dropdown

        platform_name = "Custom RTMP"          #Final design
        #platform_name = "Youtube Stream Now"  #Debugging on free restream accounts

        driver.find_element_by_xpath('//li[@data-streaming-platform-name="' + platform_name + '"]/div/button[@class="dropdown-toggle"]').click()
        # click edit settings
        driver.find_element_by_xpath('//li[@data-streaming-platform-name="' + platform_name + '"]/div/ul[@class="dropdown-menu dropdown-menu-right"]/li[1]/a[@class="jsEditChannel"]') .click()

    # try to change key
    try:
        # another check
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "jsEditChannelForm"))
        )
    except:
        driver.close()
        return -3    # Could not find settings form
    finally:
        # select key input textbox
        key = driver.find_element_by_id("editChannelKeyInput")
        # clear it
        key.clear()
        # send our key to field
        key.send_keys(newKey)
        # select and click save button
        driver.find_element_by_xpath('//form[@id="jsEditChannelForm"]/div[@class="modal-footer"]/button[@class="button button_type_action button_block"]').click()

    sleep(1)
    # close browser
    driver.close()
    return 0

