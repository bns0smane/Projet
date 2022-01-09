from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import os
import glob
from DBieee import *

# from bs4 import BeautifulSoup
# import requests
# import re
# from shutil import copyfile
# import splinter
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from pymongo import MongoClient
# import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
########################################################################

#change download directory
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

def IEEE(key):
    start_time = time.time()

    if not key:
        print('enter the keyword')
    else:    
        client = pymongo.MongoClient('localhost:27017')
        db = client.BI_PROJECTS_DB
        print('the IEEE database contains '+str(db.IEEE.count_documents({'keyWord':str(key)})))
        if db.IEEE.count_documents({'keyWord':key})!=0:
            print('the '+key+' keyword is already in the IEEE dataBase')

        else:   
            print('Scraping from IEEE...')
            chrome_options = Options()
            chrome_options.add_argument('--disable-popup-blocking')
            # chrome_options.add_argument("--kiosk")
            # chrome_options.add_argument("--headless")

            chrome_options.add_experimental_option("prefs", {
                    "download.default_directory": "<path_to_download_default_directory>",
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing_for_trusted_sources_enabled": False,
                    "safebrowsing.enabled": False,
                    "profile.default_content_settings": { "popups": 1 }
            })
            browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())

            ######################
            download_dir = "C:\\Users\\hixam\\Desktop\\scraped"
            enable_download_headless(browser, download_dir)

            url=f'https://ieeexplore.ieee.org/Xplore/home.jsp'
            browser.get(url)

            browser.find_element_by_css_selector("input[type='text']").send_keys(key)
            time.sleep(5)

            browser.find_element_by_css_selector("button[type='submit']").click()
            time.sleep(10)

            element=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME , "cc-compliance")))
            element.click()

            element=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME , "export-filter")))
            element.click()
            # time.sleep(1)

            element=WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME , "stats-SearchResults_Download")))
            element.click()
            time.sleep(3)

            ##############################################################
            #open csv file and save the keyword
            file=False
            i=0
            while(file==False):
                os.chdir('C:\\Users\\hixam\\Desktop\\scraped')
                extension = 'csv'
                all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
                # print(len(all_filenames))
                if len(all_filenames)!=0:
                    file==True
                    while(i<1):
                        for f in all_filenames:
                            filename = os.path.basename(f"C:\\Users\\hixam\\Desktop\\scraped\\{f}")
                            os.rename(filename,'IEEE.csv')
                            ff='C:\\Users\\hixam\\Desktop\\scraped\\IEEE.csv'
                            data = pd.read_csv(ff, error_bad_lines=False)
                            for i in range(0,len(data)):
                                data['keyWord']=key
                            data.to_csv("C:\\Users\\hixam\\Desktop\\scraped\\IEEE.csv", index=False)
                            file==True
                            i=2
                            break
                    break
                else:
                    print('file not found')
                    time.sleep(8)
                    file==False
            ##############################################################

            browser.quit()
            DataBase()

            os.chdir('C:\\Users\\hixam\\Desktop\\scraped')
            extension = 'csv'
            all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
            # print(len(all_filenames))
            if len(all_filenames)!=0:
                for f in all_filenames:
                    filename = os.path.basename(f"C:\\Users\\hixam\\Desktop\\scraped\\{f}")
                    os.remove(f) 
            else:
                print('file not found')

    print('--- %s  time that IEEE made'% (time.time() - start_time))

