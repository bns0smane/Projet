from itertools import zip_longest
import csv
from selenium import webdriver
# from webdriver_manager.firefox import GeckoDriverManagerkey
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import re
import pymongo
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
from shutil import copyfile
import splinter
from selenium.webdriver.chrome.options import Options
import os
import glob
from DBscopus import *
########################################################################

def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


def scopus(key):
    start_time = time.time()

    if not key:
        print('enter the keyword')
    else:         
        client = pymongo.MongoClient('localhost:27017')
        db = client.BI_PROJECTS_DB
        print('the scopus database contains '+str(db.scopus.count_documents({'keyWord':str(key)})))
        if db.scopus.count_documents({'keyWord':key})!=0:
            print('this '+key+' keyword is already in the scopus dataBase')
        else:
            print('scraping...')
            chrome_options = Options()
            # chrome_options.add_argument("--headless")
            chrome_options.add_experimental_option("prefs", {
                    "download.default_directory": "<path_to_download_default_directory>",
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing_for_trusted_sources_enabled": False,
                    "safebrowsing.enabled": False
            })

            browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())

            download_dir = "C:\\Users\\hixam\\Desktop\\scraped"
            enable_download_headless(browser, download_dir)

            url=f'https://id.elsevier.com/as/authorization.oauth2?platSite=SC%2Fscopus&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info+urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Aindv_identity&response_type=code&redirect_uri=https%3A%2F%2Fwww.scopus.com%2Fauthredirect.uri%3FtxGid%3Df3242c5f60326cc5202585cfef8f1d7b&state=forceLogin%7CtxId%3D5D90BE002C70921F717591A0566609A1.i-0e676ee53e39e14bf%3A2&authType=SINGLE_SIGN_IN&prompt=login&client_id=SCOPUS'
            browser.get(url)

            browser.find_element_by_css_selector("#bdd-email").send_keys('hicham.benosmane@etu.uae.ac.ma')
            browser.find_element_by_css_selector("#bdd-elsPrimaryBtn").click()
            time.sleep(1)

            browser.find_element_by_css_selector("#bdd-password").send_keys('azerty123')
            browser.find_element_by_css_selector("#bdd-elsPrimaryBtn").click()
            time.sleep(1)

            browser.find_element_by_css_selector(".flex-grow-1").send_keys(key)
            browser.find_element_by_css_selector("button[type='submit']").click()
            time.sleep(1)

            browser.find_element_by_css_selector("span[class='ico-navigate-down icon-after fontSizeNorm']").click()
            browser.find_element_by_xpath("//li[@id='selectAllCheck']").click()
            browser.find_element_by_xpath("//button[@id='directExport']").click()
            time.sleep(1)

            browser.find_element_by_xpath("//label[@id='exportTypeAndFormat']").click()
            browser.find_element_by_xpath("//button[@id='chunkExportTrigger']").click()

            file=False
            while(file==False) :
                file = os.path.isfile('C:\\Users\\hixam\\Desktop\\scraped\\scopus.csv')
                if(file==False):
                    print('file not found')
                else:
                    data = pd.read_csv('C:\\Users\\hixam\\Desktop\\scraped\\scopus.csv')
                    for i in range(0,len(data)):
                        data['keyWord']=key
                    data.to_csv("C:\\Users\\hixam\\Desktop\\scraped\\scopus.csv", index=False)
            browser.quit()
            DataBase()

            os.chdir('C:\\Users\\hixam\\Desktop\\scraped')
            extension = 'csv'
            all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
            if len(all_filenames)!=0:
                for f in all_filenames:
                    filename = os.path.basename(f"C:\\Users\\hixam\\Desktop\\scraped\\{f}")
                    os.remove(f) 
            else:
                print('file not found')

    print('--- %s  time that scopus made'% (time.time() - start_time))

