#!/usr/bin/env python3

from xml.dom import NotSupportedErr
from classes.parser.DeductionsParser import DeductionsParser
from classes.parser.PayrollParser import PayrollParser
from classes.reader.CSVReader import CSVReader
from classes.reader.InvoiceFileReader import InvoiceFileReader
from classes.reader.TextConsoleReader import TextConsoleReader
from pathlib import Path

import unittest
import logging
import logging.config

logger = logging.getLogger('testLogger')

class TextConsoleReaderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig(
            fname='./test/logger-tests.conf',
            disable_existing_loggers=False)

        cls.path = str(Path(__file__).parent) + "/resources/payroll"
        cls.csv = CSVReader()
        cls.csv.setDeductuctionParser(DeductionsParser())
        cls.csv.setPayrollParser(PayrollParser())
        cls.csv.setFileReader(InvoiceFileReader())
        cls.reader = TextConsoleReader(cls.csv)

    def test_read_payroll_zip_file(self):
        self.csv.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'P')
        self.assertIsNotNone(self.reader.callback_result)

    def test_read_payroll_xml_files(self):
        self.csv.file_reader.read_zipped_files(False)
        self.reader.read(self.path, 'P')
        self.assertIsNotNone(self.reader.callback_result)

    def test_read_deduction_zip_file(self):
        self.csv.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'D')
        self.assertIsNotNone(self.reader.callback_result)

    def test_read_deduction_xml_files(self):
        self.reader.read(self.path, 'D')
        self.assertIsNotNone(self.reader.callback_result)

    def test_err_not_supported(self):
        with self.assertRaises(NotSupportedErr):
            self.reader.read(self.path, 'X')
