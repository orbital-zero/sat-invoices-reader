#!/usr/bin/env python3

import logging
from pathlib import Path
from classes.reader.Callback import Callback
from classes.reader.FileReaderInterface import FileReaderInterface

import typing
import zipfile


class InvoiceFileReader(FileReaderInterface):

    def __init__(self, _is_zipped_file: bool = False) -> None:
        self._is_zipped_file = _is_zipped_file
        self._ignore_err = False

    @property
    def ignore_errors(self) -> bool:
        return self._ignore_err

    def set_ignore_errors(self, _ignore: bool):
        self._ignore_err = _ignore

    @property
    def is_zipped_file(self) -> bool:
        return self._is_zipped_file

    def read_zipped_files(self, read_zip: bool):
        self._is_zipped_file = read_zip

    def do_in_list(self, path: str, _callback: typing.Any):

        if self._is_zipped_file:
            self.__read_zip_files(path, _callback)
        else:
            self.__read_xml_files(path, _callback)

    def __read_xml_files(self, source_path: str, _callback: Callback):

        for filename in Path(source_path).glob('**/*.xml'):
            try:
                _callback.function(filename)
            except Exception as e:
                _callback.errors.append(e)
                if not self._ignore_err:
                    logging.exception(
                        'Error with file {0} , skipping...'.format(filename))

    def __read_zip_files(self, source_path: str, _callback: Callback):

        for filename in Path(source_path).glob('**/*.zip'):
            try:
                self.__read_zip_content(filename, _callback)
            except Exception as e:
                _callback.errors.append(e)
                if not self._ignore_err:
                    logging.exception(
                        'Error with file {0} , skipping...'.format(filename))
                continue

    def __read_zip_content(self, filename, _callback: Callback):

        zip_file = zipfile.ZipFile(filename)
        zipped_files = zip_file.namelist()
        file_names = [file for file in zipped_files if 'xml' in file]

        for filename in file_names:
            try:
                _callback.function(filename, zip_file)
            except Exception as e:
                _callback.errors.append(e)
                if not self._ignore_err:
                    logging.exception(
                        'Error with file {0} , skipping...'.format(filename))
                continue
