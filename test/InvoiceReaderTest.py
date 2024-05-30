#!/usr/bin/env python3

from pathlib import Path

import logging
import logging.config
import unittest

from classes.reader.InvoiceReader import InvoiceReader
from classes.reader.CustomizableFileReader import CustomizableFileReader
from classes.parser.DeductionsParser import DeductionsParser
from classes.parser.PayrollParser import PayrollParser


logger = logging.getLogger('testLogger')  

class InvoiceReaderTest(unittest.TestCase):

    @property
    def reader(self) -> InvoiceReader:   
        return self.reader

    @classmethod
    def setUpClass(self):
        logging.config.fileConfig('./test/resources/logger-tests.conf')
        self.path = str(Path(__file__).parent) + "/resources/payroll"
        self.reader = InvoiceReader()
    
    def setUp(self):
        self.reader.set_file_reader(CustomizableFileReader())
        self.reader.set_payroll_parser(PayrollParser())
        self.reader.set_deductuction_parser(DeductionsParser())

        
    def test_read_payroll_files(self):
        self.reader.file_reader.read_zipped_files(False)
        self.reader.read(self.path, 'P')
        self.__print_result(self.reader.callback.result)
        self.assertGreater(len(self.reader.callback.result), 1)

    def test_read_payroll_zip_files_show_err(self):
        self.reader.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'P')
        self.__print_result(self.reader.callback.result)
        logger.warning(self.reader.callback.errors)

        self.assertGreater(len(self.reader.callback.errors), 1)
        self.assertGreater(len(self.reader.callback.result), 1)

    def test_read_payroll_zip_files_ignore_err(self):
        self.reader.file_reader.read_zipped_files(True)
        self.reader.file_reader.set_ignore_errors(True)
        self.reader.read(self.path, 'P')
        self.assertGreater(len(self.reader.callback.result), 1)

    def test_read_deduction_files(self):
        self.reader.file_reader.read_zipped_files(False)
        self.reader.read(self.path, 'D')
        self.__print_result(self.reader.callback.result)
        self.assertGreater(len(self.reader.callback.result), 1)
        
    def test_read_deduction_zip_files(self):
        self.reader.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'D')
        self.__print_result(self.reader.callback.result)
        self.assertGreater(len(self.reader.callback.result), 1)

    def __print_result(self, _entries: list):
        """" print text entries for csv file"""
        for e in _entries:
            logger.info(e)
