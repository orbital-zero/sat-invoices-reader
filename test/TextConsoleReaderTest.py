#!/usr/bin/env python3

from xml.dom import NotSupportedErr
from classes.parser.DeductionsParser import DeductionsParser
from classes.parser.PayrollParser import PayrollParser
from classes.reader.InvoiceReader import InvoiceReader
from classes.reader.CustomizableFileReader import CustomizableFileReader
from classes.reader.TextConsoleReader import TextConsoleReader
from pathlib import Path

import logging
import logging.config
import unittest

logger = logging.getLogger('testLogger')  

class TextConsoleReaderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig('./test/resources/logger-tests.conf')

        cls.path = str(Path(__file__).parent) + "/resources/payroll"
        cls.csv = InvoiceReader()
        cls.csv.setDeductuctionParser(DeductionsParser())
        cls.csv.setPayrollParser(PayrollParser())
        cls.csv.setFileReader(CustomizableFileReader())
        cls.reader = TextConsoleReader(cls.csv)

    #@unittest.skip
    def test_list(self):
        la = ["H1","H2","H3"]
        lb = ["A","B","C"]
        le = [la, lb]
        
        final_data = self.reader.convert_to_csv(le)
        logger.info(final_data)

    def test_read_payroll_zip_file(self):
        self.csv.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'P')
        self.assertIsNotNone(self.reader.callback.result)

    def test_read_payroll_xml_files(self):
        self.csv.file_reader.read_zipped_files(False)
        self.reader.read(self.path, 'P')
        self.assertIsNotNone(self.reader.callback.result)

    def test_read_deduction_zip_file(self):
        self.csv.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'D')
        self.assertIsNotNone(self.reader.callback.result)

    def test_read_deduction_xml_files(self):
        self.reader.read(self.path, 'D')
        self.assertIsNotNone(self.reader.callback.result)

    def test_err_not_supported(self):
        with self.assertRaises(NotSupportedErr):
            self.reader.read(self.path, 'X')