#!/usr/bin/env python3

import fnmatch
from pathlib import Path
from classes.dto.Callback import Callback
from classes.reader.FileReaderInterface import FileReaderInterface
from typing import Callable

import logging
import zipfile

logger = logging.getLogger(__name__)


class CustomizableFileReader(FileReaderInterface):

    def __init__(self, _is_zipped_file: bool = False,
                 _ignore_err: bool = False) -> None:
        self._is_zipped_file = _is_zipped_file
        self._ignore_err = _ignore_err
        self._file_filter = None
        self._zip_filter = None

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

    @property
    def zip_filter(self: str) -> str:
        return self._zip_filter

    def set_zip_filter(self, _zip_filter: str):
        self._zip_filter = _zip_filter

    def do_in_list(self, path: str, _callback: Callback):
        """"Iterate files and set the callback operation to execute over each item"""

        self.__set_default_filter()
        execute = self.__get_read_function(_callback)

        for filename in Path(path).glob(self._file_filter):
            try:
                execute(filename)
            except Exception as e:
                _callback.errors.append(e)
                if not self.ignore_errors:
                    logger.error(f'Error with file {filename}, skipping...')
                continue

    def __get_read_function(self, _callback: Callback) -> Callable:
        """Get the function to read file (one to one)"""
        custom_functions = {
            "zip_func": lambda filename: self.__read_zip_content(filename, _callback),
            "file_func": lambda filename: _callback.function(filename)
        }

        return custom_functions['zip_func'] if self._is_zipped_file else custom_functions['file_func']

    def __set_default_filter(self) -> None:
        """Set default value to filter files during read"""

        if self._is_zipped_file:
            self._file_filter = self._file_filter or '**/*.zip'
            self._zip_filter = self._zip_filter or '*.xml'
        else:
            self._file_filter = self._file_filter or '**/*.xml'

    def __read_zip_content(self, file, _callback: Callback):

        with zipfile.ZipFile(file) as zip_file:
            for filename in zip_file.namelist():
                try:
                    if fnmatch.fnmatch(filename, self._zip_filter):
                        _callback.function(filename, zip_file)

                except Exception as e:
                    err_message = f"Error processing file: {filename} in {zip_file.filename}: \n {e}"
                    _callback.errors.append(err_message)
                    if not self.ignore_errors:
                        logger.error(err_message, exc_info=True)
                    continue
