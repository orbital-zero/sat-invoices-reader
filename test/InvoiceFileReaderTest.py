#!/usr/bin/env python3

import logging
import logging.config

from classes.reader.Callback import Callback
from classes.reader.InvoiceFileReader import InvoiceFileReader
from pathlib import Path

import zipfile
import unittest

logger = logging.getLogger(__name__)


class InvoiceFileReaderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_reader = InvoiceFileReader()
        cls.zip_path = str(Path(__file__).parent) + \
            "/resources/payroll/zip_file"
        cls.one_file = str(Path(__file__).parent) + \
            "/resources/payroll/one_file"
        logging.config.fileConfig(
            fname='./test/logger-tests.conf',
            disable_existing_loggers=False)

    def test_list_xml_files(self):

        callback = Callback()
        callback.set_function(
            lambda filename: self.__fault_file_callback(
                filename, callback.result))
        # self.file_reader.read_ziped_files(False)  #  False by default
        self.file_reader.do_in_list(self.one_file, callback, '**/*.xml')
        self.assertEqual(len(callback.result), 1)

    def test_list_zip_files(self):

        callback = Callback()
        fx = lambda filename, zip_file: self.__fault_zip_callback(
            filename, zip_file, callback.result)
        callback.set_function(fx)

        self.file_reader.read_zipped_files(True)
        self.file_reader.do_in_list(self.zip_path, callback, '**/*.zip')
        self.assertEqual(len(callback.result), 3)

    def __fault_file_callback(self, filename: str, _result):
        """ Append to List readed file names"""
        _result.append(filename)

    def __fault_zip_callback(
            self, filename: str, zip_file: zipfile.ZipFile, _result):
        """ Append to List readed file names in zip """
        _result.append(filename)

    def test_list_zip_callback_err(self):

        callback = Callback()
        fx = lambda filename, zip_file: self.__fault_err_callback(
            filename, zip_file)
        callback.set_function(fx)

        self.file_reader.read_zipped_files(True)
        self.file_reader.do_in_list(self.zip_path, callback, '**/*.zip')
        self.assertEqual(len(callback.errors), 3)

    def __fault_err_callback(self, filename: str, zip_file: zipfile.ZipFile):
        raise ValueError(
            'dummy error %s in %s' %
            (filename, zip_file.filename))

    def test_list_zip_callback_ignoring_err(self):

        callback = Callback()
        fx = lambda filename, zip_file: self.__fault_err_callback(
            filename, zip_file)
        callback.set_function(fx)

        self.file_reader.read_zipped_files(True)
        self.file_reader.set_ignore_errors(True)
        self.file_reader.do_in_list(self.zip_path, callback, '**/*.zip')
        self.assertEqual(len(callback.errors), 3)

    def test_err_file_callback(self):

        callback = Callback()

        def f(x):
            raise Exception('foobar')

        callback.set_function(f)

        self.file_reader.do_in_list(self.one_file, callback, '**/*.xml')
        self.assertEqual(len(callback.errors), 1)
