#!/usr/bin/env python3

from pathlib import Path
from classes.dto.Callback import Callback
from classes.reader.FileReaderInterface import FileReaderInterface
from typing import Callable

import logging
import zipfile

logger = logging.getLogger(__name__)


class CustomizableFileReader(FileReaderInterface):

    __DEFAULT_ZIP_FILTER = '**/*.zip'
    __DEFAULT_FILE_FILTER = '**/*.xml'

    def __init__(self, _is_zipped_file: bool = False,
                 _ignore_err: bool = False) -> None:
        self._is_zipped_file = _is_zipped_file
        self._ignore_err = _ignore_err
        self._file_filter = None

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

    @property
    def file_filter(self: str) -> str:
        return self._file_filter

    def set_file_filter(self, _file_filter: str):
        self._file_filter = _file_filter

    def do_in_list(self, path: str, _callback: Callback):
        """"Iterate files and set the callback operation to execute over each item"""

        self._file_filter = self.__set_default_filter()
        execute = self.__get_read_function(_callback)

        for filename in Path(path).glob(self._file_filter):
            try:
                execute(filename)
            except Exception as e:
                _callback.errors.append(e)
                if not self.ignore_errors:
                    logger.error(
                        'Error with file {0} , skipping...'.format(filename))
                continue

    def __get_read_function(self, _callback: Callback) -> Callable:
        """Get the function to read file (one to one)"""

        if self._is_zipped_file:
            return lambda filename: self.__read_zip_content(
                filename, _callback)
        else:
            return lambda filename: _callback.function(filename)

    def __set_default_filter(self) -> str:
        """"Set default value to filter files during read"""
        
        if self._file_filter is not None:
            return self._file_filter

        if(self._is_zipped_file):
            return self.__DEFAULT_ZIP_FILTER
        else:
            return self.__DEFAULT_FILE_FILTER

    def __read_zip_content(self, filename, _callback: Callback):

        zip_file = zipfile.ZipFile(filename)
        zipped_files = zip_file.namelist()
        file_names = [file for file in zipped_files if 'xml' in file]

        for filename in file_names:
            try:
                _callback.function(filename, zip_file)
            except Exception as e:
                _callback.errors.append(e)
                if not self.ignore_errors:
                    logger.error(
                        'Error with file {0} , skipping...'.format(filename))
                continue
