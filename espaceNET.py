import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
from pymongo import MongoClient
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import os
import glob
from DBespacenet import *
from toCSV import *

########################################################################

# 
# function to take care of downloading file
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

def espaceNet(key):
    start_time = time.time()

    if not key:
        print('enter the keyword')
    else:
        client = pymongo.MongoClient('localhost:27017')
        db = client.BI_PROJECTS_DB
        print('the ESPACENET database contains '+str(db.ESPACENET.count_documents({'keyWord':str(key)})))  
        
        if db.ESPACENET.count_documents({'keyWord':key})!=0:
            print('the '+key+' keyword is already in the ESPACENET dataBase')
        else:
            print('scraping...')
            chrome_options = Options()
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

            url=f'https://worldwide.espacenet.com/searchResults?submitted=true&locale=en_EP&DB=EPODOC&ST=singleline&query={key} '
            browser.get(url)

            nextPage=True
            i=1
            while(nextPage and i<5):
                time.sleep(3)

                #CSV file 
                csvFile=browser.find_element_by_css_selector('a.exportLink')
                if(csvFile):
                    csvFile.click()
                    time.sleep(1)
                    print('csv file downoalded well !!')
                else :
                    print('page'+str(i)+'  csv file not found !!')

                try:
                    next_page=element=browser.find_element(By.ID,"nextPageLinkTop")
                    if(next_page):
                        next_page.click();
                        nextPage=True
                        i+=1
                except:
                        print('all pages were scriped!!')
                        nextPage=False
                        time.sleep(1)

            browser.quit()        


            to_CSV()
            time.sleep(3)
            data=pd.read_csv('C:\\Users\\hixam\\Desktop\\scraped\\combined_csv.csv')
            for i in range(0,len(data)):
                data['keyWord']=key
            data.to_csv("C:\\Users\\hixam\\Desktop\\scraped\\combined_csv.csv", index=False)
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
    
    print('--- %s  time that EspaceNet made'% (time.time() - start_time))
    