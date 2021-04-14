import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from conf import EMAIL, PASSWORD, CHROMEDRIVER_PATH, SUBJECT_CODES


# Get the respective class path based on input
def get_class_path(subject, translate_to_lower_case=False):
    to_compare = 'translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")' \
        if translate_to_lower_case else "text()"
    try:
        return f'//div[contains({to_compare}, "{SUBJECT_CODES[subject]}")]'
    except KeyError:
        return f'//div[contains({to_compare}, "{subject}")]'


# Proceed after entering email id
def login(driver, email, password):
    # driver.find_element_by_xpath('//input[contains(@aria-label, "mail") or @id="identifierId"]').send_keys(email)
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((  # Ignoring 'E' to handle both cases
        By.XPATH, '//input[contains(@aria-label, "mail") or @id="identifierId"]'))).send_keys(email)
    wait.until(ec.element_to_be_clickable((  # Ignoring 'E' to handle both cases
        By.XPATH, '//button/*[contains(text(),"Next")]//parent::button'))).click()

    try:
        wait.until(ec.element_to_be_clickable((  # Ignoring 'P' to handle both cases
            By.XPATH, '//input[contains(@aria-label, "assword") or @type="password"]'))).send_keys(password)
    except TimeoutException:
        print("This account isn't supported perhaps because it is protected by google")
        sys.exit(-1)
    else:
        wait.until(ec.element_to_be_clickable((  # Ignoring 'E' to handle both cases
            By.XPATH, '//button/*[contains(text(),"Next")]//parent::button'))).click()  # //*[@id="passwordNext"]/div/button


if __name__ == '__main__':
    options = webdriver.ChromeOptions()  # Options to start chrome with
    # Block notifications and allow mic and camera
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2,
                                              "profile.default_content_setting_values.media_stream_mic": 1,
                                              "profile.default_content_setting_values.media_stream_camera": 1})
    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH, options=options)  # Launch chrome

    driver.implicitly_wait(10)

    driver.get("https://accounts.google.com/")
    login(driver, EMAIL, PASSWORD)

    wait = WebDriverWait(driver, 20)

    # Get the subject input and then get back to the browser
    subject = input("Enter the subject: ")
    driver.get("https://classroom.google.com/u/0/h")
    class_path = get_class_path(subject)
    if not class_path:
        print("Class Not Found :(")
        sys.exit(-1)

    # Open the class with the class path
    wait.until(ec.element_to_be_clickable((By.XPATH, class_path))).click()

    # Find and open the meet link
    link = '//div[@guidedhelpid="heroVideoCallLink"]//a[@href]'
    try:
        driver.find_element_by_xpath(link).click()
    except NoSuchElementException:
        print("No Meet Link found :(")
        input("Close the window(y/n)?: ").strip() == 'y' and driver.close()
    else:
        driver.switch_to.window(driver.window_handles[1])
        join_button = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, '//*[contains(text(), "Join now")]')))
        wait.until(ec.element_to_be_clickable((By.XPATH, '//div[contains(@aria-label, "mic")]'))).click()
        wait.until(ec.element_to_be_clickable((By.XPATH, '//div[contains(@aria-label, "camera")]'))).click()
        join_button.click()
