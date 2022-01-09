import os
import glob
import pandas as pd

def to_CSV():

    os.chdir('C:\\Users\\hixam\\Desktop\\scraped')
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    for f in all_filenames:
        os.remove(f) 

    #export to csv
    combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')
    print('CSV combined WELL !!!')

    