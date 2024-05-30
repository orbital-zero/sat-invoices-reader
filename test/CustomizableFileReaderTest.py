#!/usr/bin/env python3

import logging
import logging.config

from classes.dto.Callback import Callback
from classes.reader.CustomizableFileReader import CustomizableFileReader
from pathlib import Path

import zipfile
import unittest

logger = logging.getLogger(__name__)

class CustomizableFileReaderTest(unittest.TestCase):

    __FILTER_FOR_ZIP = '**/*.zip'
    __FILTER_FOR_XML = '**/*.xml'

    @classmethod
    def setUpClass(cls):
        resources_dir= str(Path(__file__).parent) +"/resources/"
        cls.zip_file = resources_dir + "/payroll/zip_file"
        cls.one_file = resources_dir + "/payroll/one_file"
        cls.zipped_files = resources_dir + "/payroll/zipped_files"
        logging.config.fileConfig(
            fname='./test/resources/logger-tests.conf',
            disable_existing_loggers=False)

    def setUp(self):
        '''@Before - Setup method to be executed before each test method'''
        self.file_reader = CustomizableFileReader()
        self.file_reader.set_zip_filter = "*.xml"

    def test_read_xml_file(self):
        """Test reading one xml file"""

        callback = Callback()
        callback.set_function(lambda filename:
                              self.__fault_file_callback(filename, callback.result))

        self.file_reader.set_file_filter(self.__FILTER_FOR_XML)
        self.file_reader.do_in_list(self.one_file, callback)
        self.assertEqual(len(callback.result), 1)

    def test_list_zip_content(self):
        """Test reading zip files and their content on defined path"""

        def f(filename, zip_file): self.__fault_zip_callback(filename, zip_file, callback.result)

        callback = Callback()
        callback.set_function(f)

        self.file_reader.read_zipped_files(True)
        self.file_reader.set_file_filter(self.__FILTER_FOR_ZIP)
        self.file_reader.do_in_list(self.zip_file, callback)
        self.assertEqual(len(callback.result), 3)

    def __fault_file_callback(self, filename: str, _result):
        """ Append to result list the readed file names """
        _result.append(filename)

    def __fault_zip_callback(
            self, filename: str, zip_file: zipfile.ZipFile, _result):
        """ Append to result list the readed file names in zip """
        _result.append(filename)

    def test_list_zip_callback_err(self):
        """ Test throwing exception during read files into zip, print messages in log """
        callback = Callback()
        callback.set_function(lambda filename, zip_file:
                               self.__fault_err_callback(filename, zip_file))

        self.file_reader.read_zipped_files(True)
        self.file_reader.set_file_filter(self.__FILTER_FOR_ZIP)
        self.file_reader.do_in_list(self.zip_file, callback )
        self.assertEqual(len(callback.errors), 3)

    def __fault_err_callback(self, filename: str, zip_file: zipfile.ZipFile):
        raise ValueError('dummy error %s in %s' %
            (filename, zip_file.filename))

    def test_list_zip_callback_ignoring_err(self):
        """ Test throwing exception during read files into zip, skipped messages in log """

        callback = Callback()
        callback.set_function(lambda filename,
                              zip_file: self.__fault_err_callback(filename, zip_file))

        self.file_reader.read_zipped_files(True)
        self.file_reader.set_ignore_errors(True)
        self.file_reader.set_file_filter(self.__FILTER_FOR_ZIP)
        self.file_reader.do_in_list(self.zip_file, callback)
        self.assertEqual(len(callback.errors), 3)

    def test_err_file_callback(self):
        """Test throwing exception during read xml files"""

        def f(x): raise Exception('foobar')

        callback = Callback()
        callback.set_function(f)

        self.file_reader.set_file_filter(self.__FILTER_FOR_XML)
        self.file_reader.do_in_list(self.one_file, callback)
        self.assertEqual(len(callback.errors), 1)

    def test_without_zip_fillter(self):
        """Test reading using default zip filter"""

        def f(filename, zip_file): self.__fault_zip_callback(filename, zip_file, callback.result)

        callback = Callback()
        callback.set_function(f)

        self.file_reader.set_zip_filter = None
        self.file_reader.read_zipped_files(True)
        self.file_reader.do_in_list(self.zip_file, callback)
        self.assertEqual(len(callback.result), 3)

    def test_without_xml_fillter(self):
        """Test reading using default xml filter"""
        
        def f(filename): self.__fault_file_callback(filename, callback.result)

        callback = Callback()
        callback.set_function(f)
        self.file_reader.set_file_filter(None) 
        self.file_reader.do_in_list(self.one_file, callback)
        self.assertEqual(len(callback.result), 1)
        
    def test_filter_zip_content(self):
        """Test to read a pdf file name using filters"""
        
        def f(filename, zip_file): self.__fault_zip_callback(filename, zip_file, callback.result)

        callback = Callback()
        callback.set_function(f)
        self.file_reader.read_zipped_files(True)
        self.file_reader.set_file_filter(self.__FILTER_FOR_ZIP) 
        self.file_reader._zip_filter = "*.pdf"
        self.file_reader.do_in_list(self.zipped_files, callback)
        self.assertEqual(len(callback.result), 1)