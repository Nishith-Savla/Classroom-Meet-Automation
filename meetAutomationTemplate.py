import time
from selenium import webdriver

# Get the respective class path based on input
def getClassPath(classPath):
    # You may have to change this as per your need
    if(subject == "CO" or subject == "co"): 
        classPath = '//*[@id="yDmH0d"]/div[2]/div/div[1]/div/ol/li[1]/div[1]/div[3]/h2/a[1]/div[1]'
    elif(subject == "C++" or subject == "c++"):
        classPath = '//*[@id="yDmH0d"]/div[2]/div/div[1]/div/ol/li[2]/div[1]/div[3]/h2/a[1]/div[1]'
    elif(subject == "CN" or subject == "cn"):
        classPath = '//*[@id="yDmH0d"]/div[2]/div[1]/div[1]/div/ol/li[3]/div[1]/div[3]/h2/a[1]/div[1]'
    elif(subject == "DE" or subject == "de"):
        classPath = '//*[@id="yDmH0d"]/div[2]/div[1]/div[1]/div/ol/li[4]/div[1]/div[3]/h2/a[1]/div[1]'
    else:
        print("\nEnter a valid class!!\n")
    return classPath

# Proceed after entering email id 
def enterEmail(): 
    browser.find_element_by_xpath("//*[@id='identifierId']").send_keys("YOUR EMAIL ID")
    browser.find_element_by_xpath("//*[@id='identifierNext']/div/button/div[2]").click()
    browser.implicitly_wait(10)

# Proceed after entering password
def enterPassword():
    browser.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input").send_keys("YOUR PASSWORD")
    browser.find_element_by_xpath("//*[@id='passwordNext']/div/button/div[2]").click()

option = webdriver.ChromeOptions() # Options to start chrome with
option.add_argument("--start-maximized")

# Block notifications and allow mic and camera
option.add_experimental_option("prefs", { "profile.default_content_setting_values.notifications": 2, "profile.default_content_setting_values.media_stream_mic":1 , "profile.default_content_setting_values.media_stream_camera": 1})

# Launch chrome 
browser = webdriver.Chrome(executable_path="C:/Users/nishi/chromedriver.exe", options=option)

# Go to google account login page
browser.get("https://accounts.google.com/")

# Enter email and password
enterEmail()
try:
    enterPassword()
except :
    time.sleep(5)
    enterPassword()

# Get the subject input and then get back to the browser
browser.minimize_window()
subject = input("Enter the subject: ")
browser.maximize_window()
browser.get("https://classroom.google.com/u/0/h")
classPath = ""
while(classPath == ""):
    classPath = getClassPath(classPath)

# Open the class with the class path
browser.find_element_by_xpath(classPath).click()

# Find and open the meet link
link = '//*[@id="yDmH0d"]/div[2]/div[2]/div[1]/div/div[2]/div[2]/span/a/div'
try:
    browser.find_element_by_xpath(link).click()
except:
    print("\nNo Meet Link found :(\n")
