import unittest

import sys
sys.path.append('src')

from service import get_records, get_last_run
from fetcher import *

class TestSum(unittest.TestCase):

    def test_get_records(self):
        records = get_records()
        num = len(records)
        self.assertGreater(num, 0, "Records should be greater than 0")

    def test_get_lastrun(self):
        lastrun = get_last_run()
        num = len(lastrun)
        self.assertEqual(num, 19, "Records last run timestamp should not be empty")

    def test_parse_records(self):
        from os import environ as env
        from dotenv import load_dotenv
        load_dotenv()

        fn = env['GOVTRADE_FILE']  # congress members trades filename
        records = parse(fn)
        num = len(records)
        self.assertGreater(num, 0, "# of Records parsed should be greter 0")
    

    def test_record(self):
        records = get_records()
        record = records[0]
        self.assertIsNotNone(record['lastName'], "Record should have last name")
        self.assertIsNotNone(record['firstName'], "Record should have first name")
        self.assertIsNotNone(record['filingDate'], "Record should have filing date")
        self.assertIsNotNone(record['stateDst'], "Record should have state District")
        self.assertIsNotNone(record['filingType'], "Record should have filing type")
        self.assertIsNotNone(record['docId'], "Record should have docId")
        

    def test_record_trades(self):
        records = get_records()
        record = records[0]
        self.assertGreater(len(record['trades']), 0, "Record should have trades")
    
        trades = record['trades']
        self.assertTrue('Buy' in trades or 'Sell' in trades, "Record should have trade type")

if __name__ == '__main__':
    unittest.main()
