#!/usr/bin/env python3

import logging
import logging.config
import unittest

logger = logging.getLogger(__name__)  # use 'testLogger' to print data


class LoggerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig(
            fname='./test/logger-tests.conf',
            disable_existing_loggers=False)
        logger.info("class!")

    def setUp(self):
        logger.info(
            "Before method  -------------------------------------------------")

    def tearDown(self):
        logger.info(
            "end method  -------------------------------------------------")

    #@unittest.skip
    def test_list_xml_files(self):
        logger.info("EXECUTE !")
        logger.debug('DEBUG !')
        logger.error('Error !')
        logger.critical('=( !')
