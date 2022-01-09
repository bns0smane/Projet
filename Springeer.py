from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from itertools import zip_longest
from selenium.webdriver.common.by import By
import csv
import pymongo
from pymongo import MongoClient
import time
from selenium.webdriver.support.ui import Select
import os
import glob
import pandas as pd

from DBSpringer import *
from toCSV import *

def springerr(key):
    start_time = time.time()

    if not key:
        print('enter the keyword')
    else:
 
        client = pymongo.MongoClient('localhost:27017')
        db = client.BI_PROJECTS_DB
        print('the Springer database contains '+str(db.Springer.count_documents({'keyWord':str(key)})))
        if db.Springer.count_documents({'keyWord':key})!=0:
            print('the '+key+' keyword is already in the Springer DataBase')
        else:
            start_year=2017
            end_year=2021
            print('scraping...')
            browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
            def enable_download_headless(browser,download_dir):
                browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
                params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
                browser.execute("send_command", params)
            download_dir = "C:\\Users\\hixam\\Desktop\\scraped"
            enable_download_headless(browser, download_dir)


            browser.get("https://link.springer.com/")
            browser.find_element_by_css_selector("#query").send_keys(key)
            browser.find_element_by_css_selector("#search").click()
            browser.implicitly_wait(5)
            time.sleep(7)
            try:
                browser.find_element_by_css_selector("#onetrust-accept-btn-handler").click()
            except:
                msg="no"
                time.sleep(3)
            
            for i in range(start_year,end_year):
                browser.find_element_by_css_selector(".expander-title").click()
                try:
                    browser.find_element_by_css_selector("#onetrust-accept-btn-handler").click()
                except:
                    msg="no"
                time.sleep(3)
                select = Select(browser.find_element_by_id('date-facet-mode'))
                time.sleep(5)

                select.select_by_value('in')
            
                browser.find_element_by_css_selector("#start-year").clear()
                browser.find_element_by_css_selector("#start-year").send_keys(i)
                browser.find_element_by_css_selector("#date-facet-submit").click()
                browser.find_element_by_css_selector("#tool-download").click()
                browser.find_element_by_css_selector(".remove-hover").click()


                data=pd.read_csv('C:\\Users\\hixam\\Desktop\\scraped\\SearchResults.csv')
                for i in range(0,len(data)):
                    data['keyWord']=key
                data.to_csv("C:\\Users\\hixam\\Desktop\\scraped\\SearchResults.csv", index=False)
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
                
            browser.quit()

    print('--- %s  time that Springer made'% (time.time() - start_time))
