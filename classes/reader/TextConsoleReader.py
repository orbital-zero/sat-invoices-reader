#!/usr/bin/env python3

from typing import List
from classes.reader.InvoiceReader import InvoiceReader

import logging

logger = logging.getLogger(__name__)


class TextConsoleReader:

    def __init__(self, _reader: InvoiceReader):
        self._reader = _reader

    @property
    def reader(self) -> InvoiceReader:
        return self._reader

    def set_reader(self, _reader: InvoiceReader):
        self._reader = _reader

    @property
    def callback(self) -> dict:
        return self.reader.callback

    def read(self, path: str, _type: str):

        self.reader.read(path, _type)
        formated_data = self.convert_to_csv(self.reader.callback.result)
        self.__print_list_values(formated_data)

        if(self.reader.callback.errors is not None and len(self.reader.callback.errors) >= 1):
            print("----------------------------")
            print("List of errors and warnings:")
            self.__print_list_values(self.reader.callback.errors)
            print("----------------------------")

    def __print_list_values(self, entries):
        for e in entries:
            print(e)

    def concat_values(self, values: list) -> list:
        """ Concatenate values with a field separator """
        return ["|".join(v) + "" for v in values]

    def convert_to_csv(self, invoices: list ) -> list:
        """ Concatenate values with a field separator """
        rows = []
        for item in self.concat_values(invoices):
            rows.append(item)
                
        return rows