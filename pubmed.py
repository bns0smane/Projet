from bs4 import BeautifulSoup
import requests
import time
import pymongo
import re
from pubmed_scraping import *
import sys
import os
import glob
# from timout import*
start_time = time.time()
data=[]

def PubMed(key):
    start_time = time.time()

    if not key:
        print('enter the keyword')
    else:    
        client = pymongo.MongoClient('localhost:27017')
        db = client.BI_PROJECTS_DB
        print('the PubMed database contains '+str(db.PubMed.count_documents({'keyWord':str(key)})))

        if db.PubMed.count_documents({'keyWord':key})!=0:
            print('the '+key+' keyword is already in the PubMed dataBase')
        else:
            def scrape(pmid):

                url= f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id={pmid}'
                page_ = requests.get(url)
                soup = BeautifulSoup(page_.content, 'html.parser')
                ##################################################
                attr={}  
                attr['keyWord']=key
                attr['PMID']=pmid
                attr['OWN']=soup.find('medlinecitation')['owner'] if(soup.find('medlinecitation')) else None
                attr['STAT']=soup.find('medlinecitation')['status'] if(soup.find('medlinecitation')) else None
                attr['DCOM']=soup.find('datecompleted').get_text().strip('\n') if(soup.find('datecompleted')) else None
                attr['LR']=soup.find('daterevised').get_text().strip('\n') if(soup.find('daterevised')) else None
                attr['ISSN']=[soup.find('issn').get_text() if(soup.find('issn')) else 'None' +'('+soup.find('issn')['issntype'] if(soup.find('issn')) else 'None' +')' ,soup.find('issnlinking').get_text() if(soup.find('issnlinking')) else 'None' + '(Linking)']
                attr['VI']=soup.find('volume').get_text() if(soup.find('volume')) else None
                attr['IP']=soup.find('issue').get_text() if(soup.find('issue')) else None
                attr['DP']=soup.find('pubdate').get_text() if(soup.find('pubdate')) else None
                attr['TI']=soup.find('articletitle').get_text() if(soup.find('articletitle')) else None
                attr['PG']=soup.find('medlinepgn').get_text() if(soup.find('medlinepgn')) else None
                attr['ISOABREV']=soup.find('isoabbreviation').get_text()  if(soup.find_all('isoabbreviation')) else "None"
                
                a=list(filter(None,[i.get_text() for i in soup.find_all('articleid')]))
                b=list(filter(None,[i['idtype'] for i in soup.find_all('articleid')]))
                
                attr['LID']=dict(zip(a,b))
                
                obj=soup.find_all('abstracttext')
                a=list(filter(None,[i.get_text() for i in obj]))
                b=list(filter(None,[i['label'] if(len(obj)>1) else "None" for i in obj]))
                
                attr['AB']=dict(zip(b,a))                
                attr['CI']=soup.find('copyrightinformation').get_text() if(soup.find('copyrightinformation')) else None
                obj=soup.find_all('author')
                attr['FAU']=[i.find('lastname').get_text() if(i.find('lastname')) else 'None' +', '+i.find('forename').get_text() if(i.find('forename')) else 'None' for i in obj]
                attr['AU']=[i.find('lastname').get_text() if(i.find('lastname')) else 'None' +', '+i.find('initials').get_text()  if(i.find('initials')) else 'None' for i in obj]
                attr['AD']=[i.find('affiliation').get_text() if(i.find('affiliation')) else 'None' for i in obj]
                attr['AUID']=[i.find('issue').get_text() if(i.find('issue')) else 'None' for i in obj ] 
                attr['LA']=soup.find('language').get_text() if(soup.find('language')) else 'None'
                attr['PT']=[i.get_text() for i in soup.find_all('publicationtype')]
                attr['PL']=soup.find('country').get_text() if(soup.find('country')) else 'None'
                attr['TA']=soup.find('medlineta').get_text() if(soup.find('medlineta')) else 'None'
                attr['JT']=soup.find('title').get_text() if(soup.find('title')) else 'None'
                attr['JID']=soup.find('nlmuniqueid').get_text() if(soup.find('nlmuniqueid')) else 'None'
                attr['SD']=[i.get_text() for i in soup.find_all('publicationtype')]
                attr['MH']=[i.get_text() for i in soup.find_all('meshheading')]
                attr['OT']=[i.get_text() for i in soup.find_all('keyword')]
                attr['OTO']=soup.find('keywordlist')['owner'] if(soup.find('keywordlist')) else 'None'
                attr['COIS']=soup.find('coistatement').get_text() if(soup.find('coistatement')) else 'None'
                attr['PST']=soup.find('publicationstatus').get_text() if(soup.find('keywordlist')) else 'None'  
            
                a=list(filter(None,[i.get_text() for i in soup.find_all('pubmedpubdate')]))
                b=list(filter(None,[i['pubstatus'] if(len(soup.find_all('pubmedpubdate'))>1) else "None" for i in soup.find_all('pubmedpubdate')]))
                
                attr['EDAT']=dict(zip(b,a))
                obj=soup.find_all('reference')
                
                a=list(filter(None,[i.find('citation').get_text() if(i.find('citation')) else 'None' for i in obj]))
                b=list(filter(None,[i.find('articleid').get_text() if(i.find('articleid')) else 'None' for i in obj]))
                
                attr['REFERENCES']=dict(zip(b,a))

                return attr

            def check(obj):
                if obj:
                    return obj
                else:
                    return None

            def insert_pubmed(input_):
                file_name=search_download(input_)
                client = pymongo.MongoClient('localhost:27017')
                db = client.BI_PROJECTS_DB.PubMed
                os.chdir('C:\\Users\\hixam\\Desktop\\scraped')
                extension = 'txt'
                all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
                #########################
                if len(all_filenames)!=0:
                    i=0
                    while(i<1):
                        for f in all_filenames:
                            filename = os.path.basename(f"C:\\Users\\hixam\\Desktop\\scraped\\{f}")
                            with open(f,encoding='UTF-8') as f:
                                lines = [line.rstrip() for line in f]
                                for i in lines[:2]:
                                    data.append(scrape(i))
                            i=2
                            break
                else:
                    print('file not found')
                    file==False

                try:
                    db.insert_many(data)            
                except:
                    print('an error occurred quotes were not stored to db')
                
                return False

            a= insert_pubmed(key)
    print('--- %s  time that PubMed made'% (time.time() - start_time))
