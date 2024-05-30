#!/usr/bin/env python3

from xml.dom import NotSupportedErr
from classes.parser.DeductionsParser import DeductionsParser
from classes.parser.PayrollParser import PayrollParser
from classes.reader.InvoiceReader import InvoiceReader
from classes.reader.CustomizableFileReader import CustomizableFileReader
from classes.reader.TextConsoleReader import TextConsoleReader
from pathlib import Path
from unittest.mock import patch

import logging
import logging.config
import unittest

logger = logging.getLogger('testLogger')  

class TextConsoleReaderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig('./test/resources/logger-tests.conf')
        project_dir = str(Path(__file__).parent)
        cls.path = project_dir + "/resources/payroll"
        cls._encoded_zip_files = project_dir + "/resources/payroll/zipped_files"

    def setUp(self):
        '''@Before - Setup method to be executed before each test method'''
        self.csv = InvoiceReader()
        self.csv.set_deductuction_parser(DeductionsParser())
        self.csv.set_payroll_parser(PayrollParser())
        self.csv.set_file_reader(CustomizableFileReader())
        self.reader = TextConsoleReader(self.csv)

    #@unittest.skip
    def test_list(self):
        la = ["H1","H2","H3"]
        lb = ["A","B","C"]
        le = [la, lb]
        
        final_data = self.reader.convert_to_csv(le)
        logger.info(final_data)

    @patch('builtins.print')
    def test_read_payroll_zip_file(self, mock_print):
        self.csv.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'P')
        self.assertIsNotNone(self.reader.callback.result)
        self.assertGreater(len(self.reader.callback.errors), 1)

    @patch('builtins.print')
    def test_read_payroll_xml_files(self, mock_print):
        self.csv.file_reader.read_zipped_files(False)
        self.reader.read(self.path, 'P')
        self.assertIsNotNone(self.reader.callback.result)

    @patch('builtins.print')
    def test_read_deduction_zip_file(self, mock_print):
        self.csv.file_reader.read_zipped_files(True)
        self.reader.read(self.path, 'D')
        self.assertIsNotNone(self.reader.callback.result)

    @patch('builtins.print')
    def test_read_deduction_xml_files(self, mock_print):
        self.reader.read(self.path, 'D')
        self.assertIsNotNone(self.reader.callback.result)

    def test_err_not_supported(self):
        with self.assertRaises(NotSupportedErr):
            self.reader.read(self.path, 'X')

    @patch('builtins.print')            
    def test_read_zipped_invoices_with_diff_econding(self,mock_print):
        self.csv.file_reader.read_zipped_files(True)
        self.reader.read(self._encoded_zip_files, 'P')
        self.assertGreater(len(self.reader.callback.result), 2)
        self.assertEqual(len(self.reader.callback.errors), 0)
