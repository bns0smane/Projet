import re
import time
import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import pymongo
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import glob

from selenium.webdriver.chrome.options import Options
import geckodriver_autoinstaller
chrome_options = Options()
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

def search_download(key):
    search=re.sub(" ","+",key)
    url=f'https://pubmed.ncbi.nlm.nih.gov/?term={search}&size=200&show_snippets=off'


    # Set Firefox preferences so that the file automatically saves to disk when downloaded
    chrome_options = Options()
    chrome_options.add_argument('--disable-popup-blocking')
    # chrome_options.add_argument("--kiosk")
    # chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", {
            "download.default_directory": "C:\\Users\\hixam",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,
            "profile.default_content_settings": { "popups": 1 }
    })

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())
    download_dir = "C:\\Users\\hixam\\Desktop\\scraped"
    enable_download_headless(driver,download_dir)
    
    # driver.maximize_window()
    driver.get(str(url))
    j = driver.find_element(By.ID,"save-results-panel-trigger").click()
    time.sleep(2)
    #Selecting the desired features
    #Firstly clicking on All th query results (10 000 result)
    el = driver.find_element(By.XPATH,"//select/option[@value='all-results']").click()

    #Secondly Selecting the file format (pmid in this case)
    el = driver.find_element(By.XPATH,"//select[@class='action-panel-selector']")

    for option in el.find_elements_by_tag_name('option'):
        if "PMID" in option.text:
            option.click() # select() in earlier versions of webdriver
            break

    time.sleep(4)
    #Clicking on download button
    j=driver.find_element(By.XPATH, '//button[@class="action-panel-submit"]').click()
    time.sleep(8)
    
    os.chdir('C:\\Users\\hixam\\Desktop\\scraped')
    extension = 'txt'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    if len(all_filenames)!=0:
        for f in all_filenames:
            file=f 
    else:
        print('file not found')
    
    driver.quit()
 
    return file


