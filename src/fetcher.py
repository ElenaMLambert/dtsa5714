import requests
from zipfile import ZipFile
from datetime import datetime

import sys
sys.path.append('src')

from db import *
from processor import extract_trades, convert_record

from os import environ as env
from dotenv import load_dotenv
load_dotenv()

def fetch(url, filename):
    response = requests.get(url)
    
    if response.status_code == 404:
        #print(f'skipped: {url} ')
        return None
    
    content = response.content
    if not content:
        return None

    print(f'fetching {url}')

    f = open(filename, 'wb')
    f.write(content)

    return content

def parse(filename):
    lines = None

    with ZipFile(filename) as myzip:
        with myzip.open('2024FD.txt') as myfile:
            lines = myfile.readlines()

    #columns = lines[0]
    
    records = []
    for line in lines[1:]:
        
        record = convert_record(line)
        records.append(record)

    print(f'Parsed # of records {len(records)}')

    return records

def fetch_trade_doc(docId):
    gtUrl = env['GOVTRADE_URL']
    url = f'{gtUrl}/{docId}.pdf'
    
    outfn = f'/tmp/{docId}.pdf' # trades file of the record
    resp = fetch(url, outfn)
    #resp = True
    
    if resp:
        return extract_trades(outfn)
    

def fetch_trades(records):

    for record in records:
        docId = record['docId']
        trades = fetch_trade_doc(docId) # fetch individual trade doc
        
        if not trades:
            trades = ''
        
        record['trades'] = trades
        
        if record['lastName'] == 'Pelosi':
            print(record)


def save_records(records):
    #print(f'saving # records {len(records)}')
    for record in records:
        insert_record(record)

#@scheduler.task('cron', id='do_job_3', week='*', day_of_week='sun')
def main():
    url = env['GOVTRADELIST_URL']
    fn = env['GOVTRADE_FILE']  # congress members trades filename
    
    fetch(url, fn) # fetch gov trades list

    records = parse(fn)
    fetch_trades(records) # fetch individual trade doc per record

    init()
    save_records(records)
    close()

    f = open('/tmp/gt_lastrun','w')
    f.write(f'{datetime.now()}')
    f.close()

    print('Job  executed')

if __name__ == '__main__' :
    main()
    
