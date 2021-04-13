import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from conf import EMAIL, PASSWORD, CHROMEDRIVER_PATH, SUBJECT_CODES


# Get the respective class path based on input
def get_class_path(subject, translate_to_lower_case=False):
    # You may have to change this as per your need
    # if subject.casefold() == "co":
    #     class_path = '//*[@id="yDmH0d"]/div[2]/div/div[1]/div/ol/li[1]/div[1]/div[3]/h2/a[1]/div[1]'
    # elif subject.casefold() == "c++":
    #     class_path = '//*[@id="yDmH0d"]/div[2]/div/div[1]/div/ol/li[2]/div[1]/div[3]/h2/a[1]/div[1]'
    # elif subject.casefold() == "cn":
    #     class_path = '//*[@id="yDmH0d"]/div[2]/div[1]/div[1]/div/ol/li[3]/div[1]/div[3]/h2/a[1]/div[1]'
    # elif subject.casefold() == "de":
    #     class_path = '//*[@id="yDmH0d"]/div[2]/div[1]/div[1]/div/ol/li[4]/div[1]/div[3]/h2/a[1]/div[1]'
    # else:
    #     print("Enter a valid class!!")
    to_compare = f'translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")' \
        if translate_to_lower_case else "text()"
    try:
        return f'//div[contains({to_compare}, "{SUBJECT_CODES[subject]}")]'
    except KeyError:
        return None


# Proceed after entering email id
def login(driver, email, password):
    # driver.find_element_by_xpath('//input[contains(@aria-label, "mail") or @id="identifierId"]').send_keys(email)
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((  # Ignoring 'E' to handle both cases
        By.XPATH, 'input[contains(@aria-label, "mail") or @id="identifierId"]'))).send_keys(email)
    next_button = driver.find_element_by_xpath(
        '//button/*[contains(text(),"Next")]')
    next_button.click()  # //*[@id="identifierNext"]/div/button

    try:
        wait.until(ec.presence_of_element_located((  # Ignoring 'P' to handle both cases
            By.XPATH, 'input[contains(@aria-label, "assword") or @type="password"]'))).send_keys(password)
    except TimeoutException:
        print("This account isn't supported perhaps because it is protected by google")
        sys.exit(-1)
    else:
        next_button.click()  # //*[@id="passwordNext"]/div/button


if __name__ == '__main__':
    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH, options=options)  # Launch chrome
    options = webdriver.ChromeOptions()  # Options to start chrome with
    options.add_argument("--start-maximized")
    # Block notifications and allow mic and camera
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2,
                                              "profile.default_content_setting_values.media_stream_mic": 1,
                                              "profile.default_content_setting_values.media_stream_camera": 1})
    # Go to google account login page
    driver.get("https://accounts.google.com/")
    login(driver, EMAIL, PASSWORD)  # Login to google account

    # Get the subject input and then get back to the browser
    # driver.minimize_window()
    subject = input("Enter the subject: ")
    # driver.maximize_window()
    driver.get("https://classroom.google.com/u/0/h")
    class_path = get_class_path(subject)
    if not class_path:
        print("Class Not Found :(")
        sys.exit(-1)

    # Open the class with the class path
    driver.find_element_by_xpath(class_path).click()

    # Find and open the meet link
    link = '//*[@id="yDmH0d"]/div[2]/div[2]/div[1]/div/div[2]/div[2]/span/a/div'
    try:
        driver.find_element_by_xpath(link).click()
    except NoSuchElementException:
        driver.minimize_window()
        print("No Meet Link found :(")
