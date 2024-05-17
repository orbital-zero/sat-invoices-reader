#!/usr/bin/env python3

from classes.manager.InvoiceClassifier import InvoiceClassifier
from classes.parser.GeneralInvoiceParser import GeneralInvoiceParser
from classes.reader.CustomizableFileReader import CustomizableFileReader
from pathlib import Path

import logging
import logging.config
import unittest
import os
import datetime

logger = logging.getLogger("testLogger")


class InvoiceClassifierTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_path = Path(__file__).parent
        cls.source_path = str(base_path) + "/resources/payroll/two_files"
        cls.output_path = os.path.join(str(base_path.parent), "target")
        logging.config.fileConfig(fname='./test/resources/logger-tests.conf', disable_existing_loggers=False)

    def setUp(self):
        '''@Before - Setup method to be executed before each test method'''
        self.manager = InvoiceClassifier()
        self.manager.set_invoice_parser(GeneralInvoiceParser())
        self.file_reader = CustomizableFileReader(False, False)
        self.file_reader.set_zip_filter = "*.xml"
        self.manager.set_file_reader(self.file_reader) 

    def test_classify_invoices_with_original_names(self):

        self.manager.classify(self.source_path, self.__get_temp_out_path(), '*.xml')

        self.assertEqual(len(self.manager.callback.errors), 0)
        self.__validate_existing_files(self.manager.callback.result)
        
    def test_classify_invoices_with_new_names(self):

        self.manager.set_rename_files(True)
        self.manager.classify(self.source_path, self.__get_temp_out_path(), '*.xml')

        self.assertEqual(len(self.manager.callback.errors), 0)
        self.__validate_existing_files(self.manager.callback.result)

    def test_classify_zipped_invoices_with_original_names(self):

        self.manager.classify(self.source_path, self.__get_temp_out_path(), '*.zip')

        self.assertEqual(len(self.manager.callback.errors), 0)
        self.__validate_existing_files(self.manager.callback.result)
            
    def test_classify_zipped_invoices_with_new_names(self):

        self.manager.set_rename_files(True)
        self.manager.classify(self.source_path, self.__get_temp_out_path(), '*.zip')

        self.assertEqual(len(self.manager.callback.errors), 0)
        self.__validate_existing_files(self.manager.callback.result)

    def __get_temp_out_path(self) -> str:
        # Get the current date
        return os.path.join(self.output_path, datetime.datetime.now().strftime("%Y%m%d%H%M_%S%f"))
    
    def __validate_existing_files(self, _files):
        for f in _files:
            self.assertTrue(os.path.exists(f))
