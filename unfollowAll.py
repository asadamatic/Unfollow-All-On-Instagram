from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import getpass
import sys
import time

option = Options()

#Adding attributes to the browser to be openned
option.add_argument('--disable-infobars')
option.add_argument('start-maximized')
option.add_argument('--disable-extensions')
option.add_argument('--disable-notifications')

#Click 'Block' option on browser notification that asks for 'Push notifications' permission
option.add_experimental_option('prefs', { 'profile.default_content_setting_values.notifications': 2})   

print('Provide your login credentials!')
username = input('Username: ')
password = getpass.getpass()

browser = webdriver.Chrome(options=option)

unfollowedCheck = 0 #Check for number of accounts unfollowed

#Adding a delay, and waiting for the element to be loaded
delay = 10
wait = WebDriverWait(browser, delay)

browser.get('https://www.instagram.com/accounts/login/?next=%2F{}%2F&source=desktop_nav'.format(username))

time.sleep(4)

try:
    #Referencing text box that asks for email
    usernameInput = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
    usernameInput.send_keys(username)
    
    #Referencing text box that asks for password
    passwordInput = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')
    passwordInput.send_keys(password)

    #Referencing Login Button
    loginButton = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')
    loginButton.click()

    time.sleep(4)

    try:
        
        #Looking for a login error message
        errorMessagePresent = browser.find_element_by_xpath('//*[@id="slfErrorAlert"]')
      
        print('Wrong Credentials :(')
        sys.exit() #exit the program

    except  (NoSuchElementException, TimeoutException) as exception:

        print('Successfuly Loggedin :)')  
          

except (NoSuchElementException, TimeoutException) as exception:

    print("Slow Or No Connection :(")
    sys.exit()





try:
    
    numberOffollowed = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span')))
    followed = numberOffollowed.text
    followed = int(int(followed) + 1)

except (NoSuchElementException, TimeoutException) as exception:
    
    print("Slow Or No Connection :(")
    sys.exit()


try:
    
    followingList = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]')))
    followingList.click()

    time.sleep(2)

    for i in range(1, followed):

        try:

            unFollowButton = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[3]/button'.format(i))))
            unFollowButton.click()                                                      
                                              
            time.sleep(2) #two second delay

            unFollowConfirm = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div[3]/button[1]')))
            unFollowConfirm.click()

            time.sleep(2)

            unfollowedCheck = i

        except (NoSuchElementException, TimeoutException) as exception:

            #Break the loop if there are no more accounts being followed
            break
        
except (NoSuchElementException, TimeoutException) as exception:
    print('Slow Or No Connection :(')

try:
    #Closing the pop up box, showing accounts followed by the user
    closeFollowingList =wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[1]/div/div[2]')))
    closeFollowingList.click()

except (NoSuchElementException, TimeoutException) as exception:
    pass

followed = followed - 1
#Making sure, all the accounts have been unfollowed
if unfollowedCheck == followed:

    print('Unfollowed All Successfully :)')
    sys.exit()