# Import dependencies
import os
from dotenv import load_dotenv
from splinter import Browser
import time
from selenium import webdriver

# Load env to retrieve hidden variables
load_dotenv()
executable_path=os.getenv('executable_path')
User=os.getenv('funds_User')
Password=os.getenv('funds_Pass')

# Create csv folder in case it doesn't exist.
parent_dir = os.getcwd()
outputPath = os.path.join(parent_dir, 'csv')
try:
    os.mkdir(outputPath)
except:
    pass

# URL to scrap:
loginURL='https://www.addmorefunds.com/login/'
fundsURL='https://www.addmorefunds.com/nft/nba-top-shot/'

# Function to initilize browser
def initBrowser(exPath, outputPath, headless=False):
    exPath = {"executable_path": exPath}
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory" : outputPath,
        "download.directory_upgrade": "true",
        "download.prompt_for_download": "false",
        "disable-popup-blocking": "true"

    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    
    return Browser("chrome", **exPath, headless=headless, options=options)

# Log In function
def fundsLogin(url,browser):
    browser.visit(url)
    browser.fill('username', User)
    browser.fill('password', Password)
    browser.find_by_value('Sign In').click() 


# Function to download the CSVs
def DownlowadCSV(browser):
    target1='button[title="Click for sale history."]'
    target2='button[title="Download CSV"]'
    target3='button[aria-label="Close"]'
    advancepage=browser.find_by_tag('div[class="text-left col-4"]').find_by_tag('button[class="btn btn-secondary"]').first
    for page in range(1,13):
        if browser.is_element_visible_by_css(target1, wait_time=25):
            sold_history=browser.find_by_css(target1)
            for s in sold_history:
                try:
                    s.click()
                    if browser.is_element_visible_by_css(target2, wait_time=25):
                        try:
                            export=browser.find_by_css(target2)
                            export.mouse_over()
                            export.click()
                        except Exception as e:
                            print(f'"Export" element error on page {page}.\n{e}')
                    else:
                        print(f'"Export" element not visible on page {page}.\n')
                    if browser.is_element_visible_by_css(target3, wait_time=25):
                        try: 
                            c=browser.find_by_css(target3)
                            c.mouse_over()
                            c.click()
                        except Exception as e:
                            print(f'"Close element error on page {page}:\n{e}')
                    else:
                        print(f'"Close" element not visible on page {page}.\n')
                               
                except Exception as e:   
                    print(f'"Sold History" element error on page {page}.\n{e}')
                        
                                  
            advancepage.click()            
            time.sleep(1)
            browser.execute_script("window.scrollTo(0, 0);")
            if (page % 2) == 0:
                time.sleep(6)
            else:
                time.sleep(3)
                              
# Function to initialize the scrap
def OneTopShot(url1, url2):
    browser = initBrowser(executable_path, outputPath, False)
    fundsLogin(url1, browser)
    time.sleep(1)
    browser.visit(url2)
    time.sleep(1)
    DownlowadCSV(browser)
    time.sleep(2)
    browser.execute_script("var message; message= 'Download Complete!'; window.alert(message);")

# Initialize the script

if __name__ == "__main__":
    OneTopShot(loginURL, fundsURL)
   