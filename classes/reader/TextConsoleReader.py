#!/usr/bin/env python3

from classes.reader.CSVReader import CSVReader

import logging

logger = logging.getLogger(__name__)  

class TextConsoleReader:

    def __init__(self, _reader: CSVReader):
        self._reader = _reader

    @property
    def reader(self) -> CSVReader:
        return self._reader
    
    def set_reader(self, _reader: CSVReader):
        self._reader = _reader

    @property
    def callback_result(self) -> dict:
        return self.reader.callback_result

    def read(self, path: str, _type: str):

        self.reader.read(path, _type)
        self.__print_csv_content(self.reader.callback_result)

        if(self.reader.callback.errors is not None and len(self.reader.callback.errors)>=1):
            print("----------------------------")
            print("List of errors and warnings:")
            self.__print_errors(self.reader.callback.errors)
            print("----------------------------")

    def __print_csv_content(self, callback_result: list):
        """" print text entries for csv file"""
        for entries in callback_result:
            for e in entries:
                print(e)

    def __print_errors(self, entries):
        for e in entries:
            print(e)
