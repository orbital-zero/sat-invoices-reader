#!/usr/bin/env python3

from pathlib import Path

import logging
import logging.config
import unittest

from classes.reader.CSVReader import CSVReader
from classes.reader.InvoiceFileReader import InvoiceFileReader
from classes.parser.DeductionsParser import DeductionsParser
from classes.parser.PayrollParser import PayrollParser

logger = logging.getLogger('testLogger')  

class CSVReaderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig(fname='./test/logger-tests.conf', disable_existing_loggers=False)
        cls.path = str(Path(__file__).parent) + "/resources/payroll"
        #cls.path = 'C:/Users/003084781/Downloads/SAT/Sueldos/03'
        cls.reader = CSVReader()
        cls.reader.setFileReader(InvoiceFileReader())
    
    def setUp(self):
        self.reader.setPayrollParser(PayrollParser())
        self.reader.setDeductuctionParser(DeductionsParser())

    @unittest.skip
    def test_list(self):
        la = ["A","B","C"]
        lb = ["A","B","C"]
        le = []
        le.append(la)
        le.append(lb)

        final_data = ["|".join(w) + "\n" for w in le]
        logger.info(final_data)
        
    def test_read_payroll_files(self):
        self.reader.file_reader.read_zipped_files(False)
        self.reader.read(self.path, 'P')
        #self.__print_csv_content(self.reader.callback_result)
        print(self.reader.callback.errors)
        self.assertGreater(len(self.reader.callback_result[0]), 1)

    def test_read_payroll_zip_files_show_err(self):
        self.reader.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'P')
        #self.__print_csv_content(self.reader.callback_result)
        logger.warn(self.reader.callback.errors)
        self.assertGreater(len(self.reader.callback.errors), 1)
        self.assertGreater(len(self.reader.callback_result[0]), 1)

    def test_read_payroll_zip_files_ignore_err(self):
        self.reader.file_reader.read_zipped_files(True)
        self.reader.file_reader.set_ignore_errors(True)
        self.reader.read(self.path, 'P')
        #logger.info(self.reader.callback.errors)
        self.assertGreater(len(self.reader.callback_result[0]), 1)

    def test_read_deduction_files(self):
        self.reader.file_reader.read_zipped_files(False)
        self.reader.read(self.path, 'D')
        #self.__print_csv_content(self.reader.callback_result)
        self.assertGreater(len(self.reader.callback_result[0]), 1)
        
    def test_read_deduction_zip_files(self):
        self.reader.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'D')
        #self.__print_csv_content(self.reader.callback_result)
        self.assertGreater(len(self.reader.callback_result[0]), 1)

    def __print_csv_content(self, callback_result: list):
        """" print text entries for csv file"""
        for entries in callback_result:
            for e in entries:
                print(e)