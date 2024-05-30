#!/usr/bin/env python3

import logging
import logging.config
import unittest
import logging

#logger = logging.getLogger('testLogger') # use 'testLogger' to print data

class LoggerTest(unittest.TestCase):

    #fileConfig('logging_config.ini')
    logger = logging.getLogger('testLogging')

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig('./test/resources/logger-tests.conf')
        

    def setUp(self):
        self.logger.info(
            "Before method  -------------------------------------------------")
        self.logger.info(__name__)

    def tearDown(self):
        self.logger.info(
            "end method  -------------------------------------------------")

    #@unittest.skip
    def test_list_xml_files(self):
        self.logger.info("EXECUTE !")
        self.logger.debug('DEBUG !')
        self.logger.error('Error !')
        self.logger.critical('=( !')