import sys
import time

from selenium import webdriver


# Get the respective class path based on input
def get_class_path(classPath):
    # You may have to change this as per your need
    if subject.casefold() == "co":
        classPath = '//*[@id="yDmH0d"]/div[2]/div/div[1]/div/ol/li[1]/div[1]/div[3]/h2/a[1]/div[1]'
    elif subject.casefold() == "c++" :
        classPath = '//*[@id="yDmH0d"]/div[2]/div/div[1]/div/ol/li[2]/div[1]/div[3]/h2/a[1]/div[1]'
    elif subject.casefold() == "cn" :
        classPath = '//*[@id="yDmH0d"]/div[2]/div[1]/div[1]/div/ol/li[3]/div[1]/div[3]/h2/a[1]/div[1]'
    elif subject.casefold() == "de" :
        classPath = '//*[@id="yDmH0d"]/div[2]/div[1]/div[1]/div/ol/li[4]/div[1]/div[3]/h2/a[1]/div[1]'
    else:
        print("\nEnter a valid class!!\n")
    return classPath

# Proceed after entering email id 
def enter_email(): 
    browser.find_element_by_xpath("//*[@id='identifierId']").send_keys("YOUR EMAIL ID")
    browser.find_element_by_xpath("//*[@id='identifierNext']/div/button/div[2]").click()
    browser.implicitly_wait(10)

# Proceed after entering password
def enter_password():
    browser.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input").send_keys("YOUR PASSWORD")
    browser.find_element_by_xpath("//*[@id='passwordNext']/div/button/div[2]").click()

option = webdriver.ChromeOptions() # Options to start chrome with
option.add_argument("--start-maximized")

# Block notifications and allow mic and camera
option.add_experimental_option("prefs", { "profile.default_content_setting_values.notifications": 2, "profile.default_content_setting_values.media_stream_mic":1 , "profile.default_content_setting_values.media_stream_camera": 1})

# Launch chrome 
browser = webdriver.Chrome(executable_path="YOUR CHROMEDRIVER PATH", options=option)

# Go to google account login page
browser.get("https://accounts.google.com/")

# Enter email and password
enter_email()
try:
    enter_password()
except :
    try:
        time.sleep(5)
        enter_password()
    except:
        browser.minimize_window()
        print("This account isn't supported perhaps because it is protected by google")
        sys.exit(-1)

# Get the subject input and then get back to the browser
browser.minimize_window()
subject = input("Enter the subject: ")
browser.maximize_window()
browser.get("https://classroom.google.com/u/0/h")
classPath = ""
while(classPath == ""):
    classPath = get_class_path(classPath)

# Open the class with the class path
browser.find_element_by_xpath(classPath).click()

# Find and open the meet link
link = '//*[@id="yDmH0d"]/div[2]/div[2]/div[1]/div/div[2]/div[2]/span/a/div'
try:
    browser.find_element_by_xpath(link).click()
except:
    browser.minimize_window()
    print("\nNo Meet Link found :(\n")
