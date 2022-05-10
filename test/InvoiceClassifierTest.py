#!/usr/bin/env python3

from classes.manager.InvoiceClassifier import InvoiceClassifier
from classes.parser.GeneralInvoiceParser import GeneralInvoiceParser
from classes.reader.InvoiceFileReader import InvoiceFileReader
from pathlib import Path

import logging
import logging.config
import unittest
import os

logger = logging.getLogger(__name__)


class InvoiceClassifierTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manager = InvoiceClassifier()
        cls.manager.set_file_reader(InvoiceFileReader(False, True))
        cls.manager.set_invoice_parser(GeneralInvoiceParser())
        base_path = Path(__file__).parent
        cls.source_path = str(base_path)+"/resources/payroll/two_files"
        cls.output_path = str(base_path.parent)+os.path.sep+"target"
        logging.config.fileConfig(fname='./test/logger-tests.conf', disable_existing_loggers=False)

    def test_classify_invoices(self):

        self.manager.classify(self.source_path, self.output_path, '*.xml')
        self.assertEqual(len(self.manager.callback_errors), 0)

        for r in self.manager.callback_result:
            self.assertTrue(Path(r).exists)

    def test_classify_zipped_invoices(self):

        self.manager.classify(self.source_path, self.output_path, '*.zip')
        self.assertEqual(len(self.manager.callback_errors), 0)

        for r in self.manager.callback_result:
            self.assertTrue(Path(r).exists)
