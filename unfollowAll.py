from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import sys
import time
from getpass import getpass

from si_to_int import convert_si_to_number

option = Options()

#Adding attributes to the browser to be openned
option.add_argument('--disable-infobars')
option.add_argument('start-maximized')
option.add_argument('--disable-extensions')
option.add_argument('--disable-notifications')

#Click 'Block' option on browser notification that asks for 'Push notifications' permission
option.add_experimental_option('prefs', { 'profile.default_content_setting_values.notifications': 2})   

print('Provide your login credentials!')
username = input('Enter your username: ')
password = getpass()

#Number of users unfollowed
unFollowed = 0


browser = webdriver.Chrome(options=option)

unFollowedCheck = 0 #Check for number of accounts unfollowed

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



    try:

        #Referencing text box that asks for email
        usernameInput = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
        usernameInput.send_keys(username)
    
        #Referencing text box that asks for password
        passwordInput = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
        passwordInput.send_keys(password)

        #Referencing Login Button
        loginButton = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button')
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

    #Converting Units 'k', 'm' and 'b' into numbers
    followed = convert_si_to_number(followed)

except (NoSuchElementException, TimeoutException) as exception:
    
    print("Slow Or No Connection :(")
    sys.exit()


try:
    
    followingList = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]')))
    followingList.click()

    time.sleep(2)

    followedPopup = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))

    for unFollowedCheck in range(1, 30):

        try:

            if unFollowedCheck <= 6:

                unFollowButton = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[3]/button'.format(unFollowedCheck))))  
                                                                                                                                                         
            
                usernameUnFollowed = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[2]/div[1]/div/div/a'.format(unFollowedCheck))))
                                                                                                        
            else:

                unFollowButton = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[2]/button'.format(unFollowedCheck))))
                                                                                                   
                usernameUnFollowed = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a'.format(unFollowedCheck))))
                                 


            if unFollowButton.text == 'Following':

                unFollowButton.click()   

                time.sleep(1)

                #confirming to unfollow the selected user
                unFollowConfirm = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div[3]/button[1]')))
                unFollowConfirm.click()


                print('Unfollowed {}'.format(usernameUnFollowed.text))   

                time.sleep(4)

                #Detecting if Instagram is blocking more unfollows
                if unFollowButton.text == 'Follow':
                    
                    unFollowed = unFollowed + 1

                elif unFollowButton.text == 'Following':
                    
                    print('Instagram is blocking this action at the moment, try again later :)')
                    break 
            else:

                #Interpreting this condition as the end of 'Following' list
                break                
            

            if unFollowedCheck % 6 == 0: #Scrolling on Followers popup after unfollowing 7 users every time 
                browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', followedPopup)
                print('Scrolling...')
                time.sleep(2)


        except (NoSuchElementException, TimeoutException) as exception:
            
            #Break the loop if there are no more accounts being followed
            print('Some error occured :(')
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
if unFollowed == followed:

    print('Unfollowed All {} Users Successfully :)'.format(unFollowed))
    sys.exit()

else:

    print('Unfollowed {} users.'.format(unFollowed))


sys.exit()
