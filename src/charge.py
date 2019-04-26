from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def clicker(input, context):

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--single-process')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = "./bin/headless-chromium"

    driver_path = './bin/chromedriver'

    browser = webdriver.Chrome(driver_path, chrome_options=options)

    # navigate to the home url

    browser.get('https://na.chargepoint.com/home')

    login_usr = ''
    password = ''
    waitlist_name = ''

    # log in to chargepoint with credentials

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'user_name'))).send_keys(login_usr)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'user_password'))).send_keys(password)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'validate-login'))).click()

    # go to waitlist

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'i_community'))).click()

    # go only to saved_waitlist section

    saved_waitlist_block = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'join_has_saved_waitlists')))

    saved_waitlists = WebDriverWait(saved_waitlist_block, 10).until(EC.presence_of_element_located((By.XPATH, './/ul[@class="waitlist_list_container station_rows"]')))

    waitlists = WebDriverWait(saved_waitlists, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'waitlist_list_item')))

    for waitlist in waitlists:

        name = waitlist.find_element_by_xpath('.//div[@class="waitlist_item_top"]').text

        # check if the element can be found! If not -> move on!

        if name is None:
            print('Waitlist not able to be found at this time!')
            pass
        else:
            if waitlist_name == name:
                # click on the Join button
                WebDriverWait(waitlist, 10).until(EC.presence_of_element_located((By.ID, 'saved_waitlist_button_text'))).click()
                # click on the Okay button
                submit_okay = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/button[@class="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only"]')))
                # it looks like there are two elements with the same xpath, one of them is hidden. so got to take the second one!
                submit_okay[1].click()
                print('Successfully entered on the waitlist!')
                # end the loop
                break
            else:
                print('Waitlist Spot doesn\'t match!')

    # exit & close browser after everything!

    browser.close()

if __name__ == '__main__':
    clicker(None, None)
