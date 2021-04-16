# Import dependencies
import os
from dotenv import load_dotenv
from splinter import Browser
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs

# Load env to retrieve hidden variables
load_dotenv()
chrome_path=os.getenv('chromedriver')
firefox_path=os.getenv('geckodriver')
User=os.getenv('funds_User')
Password=os.getenv('funds_Pass')
exPath={1: chrome_path, 2: firefox_path}

# Create a new folder each time the script is run, named with the current date and time
seconds = time.time()
today=time.ctime(seconds)
date = today.replace(" ", "_")
outputfolder = date.replace(":", ".")

# Create csv folder in case it doesn't exist.
parent_dir = os.getcwd()
outputPath = os.path.join(parent_dir, outputfolder)
try:
    os.mkdir(outputPath)
except:
    print('Folder already exists.')

# URL to scrap:
loginURL='https://www.addmorefunds.com/login/'
fundsURL='https://www.addmorefunds.com/nft/nba-top-shot/'

# Function to initilize Chrome browser
def initChrome(executablePath, outputPath):
    expath = {"executable_path": executablePath}
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
    
    return Browser("chrome", **expath, headless=False, options=options)

# Function to initilize Firefox browser
def initFirefox(executablePath, outputPath):
    expath = {"executable_path": executablePath}
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", outputPath)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                           "text/plain,text/csv,application/csv,application/download,application/octet-stream")
    profile.set_preference("browser.download.manager.showAlertOnComplete", False)
    profile.set_preference("browser.download.panel.shown", False)
    profile.update_preferences()
    return Browser("firefox", profile, **expath, headless=False)

# Function to select the browser to initialize
def initBrowser(exPath, downloadFolder):
    browserType = {1: "Chrome", 2: "Firefox"}
    driver = int(input('Which browser would you like to use (1: Chrome, 2: Firefox)? '))
    if driver==1:
        browser=initChrome(exPath[1], downloadFolder)
        return browser
    elif driver==2:
        browser=initFirefox(exPath[2], downloadFolder)
        return browser
    else:
        print('\n\nPlease enter the right option (1: Chrome, 2: Firefox). ')
        initBrowser(exPath, downloadFolder)
        
# Log In function
def fundsLogin(url,browser):
    browser.visit(url)
#     removeBanner(browser)
    browser.fill('username', User)
    browser.fill('password', Password)
    browser.find_by_value('Sign In').click() 


# Function to download the CSVs
def DownlowadCSV(browser, numpages):
    removeBanner(browser)
    target1='button[title="Click for sale history."]'
    target2='button[title="Download CSV"]'
    target3='button[aria-label="Close"]'
    advancepage=browser.find_by_tag('div[class="text-left col-4"]').find_by_tag('button[class="btn btn-secondary"]').first
    for page in range(1,numpages):
        print(f'\nStart downloads in page {page}\n', flush=True)
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
                            time.sleep(2)
                        except Exception as e:
                            print(f'"Export" element error on page {page}.\n{e}', flush=True)
                    else:
                        print(f'"Export" element not visible on page {page}.\n', flush=True)
                    if browser.is_element_visible_by_css(target3, wait_time=25):
                        try: 
                            c=browser.find_by_css(target3)
                            c.mouse_over()
                            c.click()
                            time.sleep(1)
                        except Exception as e:
                            print(f'"Close element error on page {page}:\n{e}', flush=True)
                    else:
                        print(f'"Close" element not visible on page {page}.\n', flush=True)
                               
                except Exception as e:   
                    print(f'"Sold History" element error on page {page}.\n{e}', flush=True)
                        
            print(f'Finished downloads in page {page}\n', flush=True)                      
            advancepage.click()            
            time.sleep(1)
            browser.execute_script("window.scrollTo(0, 0);")
            if (page % 2) == 0:
                time.sleep(4)
            else:
                time.sleep(2)

# Function to find the number of pages on nbatopshop
def Page(browser):
    html = browser.html
    soup=bs(html, 'html.parser')
    strong=soup.find('strong').text
    numpages=int(strong[-2:])
    return numpages

# Remove new banner
def removeBanner(browser):
    browser.execute_script("window.scrollTo(0, 0);")
    target0='button[aria-label="Close"]'
    if browser.is_element_visible_by_css(target0, wait_time=25):      
        banner2=browser.find_by_css(target0)  
        banner2.mouse_over()
        banner2.click()
        time.sleep(1)
        
# Function to initialize the scrap
def NBATopShot(url1, url2, exPath):
    browser = initBrowser(exPath, outputPath)
    fundsLogin(url1, browser)
    time.sleep(1)
    browser.visit(url2)
    time.sleep(2)
    # remove banner	
    removeBanner(browser)
    time.sleep(1)
    # continue script
    numpages=Page(browser)
    time.sleep(1)
    start=time.time()
    DownlowadCSV(browser, numpages)
    end=time.time()
    totalseconds=end-start
    total=time.gmtime(totalseconds)       
    time.sleep(1)
    js = f'var message; message= "Download Complete in {total[3]} hours {total[4]} minutes {total[5]} seconds", window.alert(message);'
    time.sleep(1)           
    browser.execute_script(js)
    
# Initialize the script
if __name__ == "__main__":
    try:
        NBATopShot(loginURL, fundsURL, exPath)
    except Exception as e:
        print(e, flush=True)  