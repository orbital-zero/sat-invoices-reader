#!/usr/bin/env python3

from pathlib import Path
from xml.etree.ElementTree import ElementTree
from classes.dto.Comprobante import Comprobante
from classes.parser.CustomElement import CustomElement
from classes.parser.InvoiceParserInterface import InvoiceParserInterface
from classes.dto.Callback import Callback
from classes.reader.FileReaderInterface import FileReaderInterface
from lxml import etree

import re
import shutil
import logging
import zipfile
import os

logger = logging.getLogger(__name__)


class InvoiceClassifier:

    __DATE_PATTERN = r"(\d{4})[/.-](\d{2})[/.-](\d{2})"

    @property
    def file_reader(self) -> FileReaderInterface:
        return self._reader

    def set_file_reader(self, _reader: FileReaderInterface):
        self._reader = _reader

    @property
    def invoice_parser(self) -> InvoiceParserInterface:
        return self._invoice_parser

    def set_invoice_parser(self, _invoice_parser: InvoiceParserInterface):
        self._invoice_parser = _invoice_parser

    @property
    def callback(self) -> Callback:
        return self._callback

    def set_callback(self, _callback: Callback):
        self._callback = _callback

    @property
    def rename_files(self) -> bool:
        return self._rename_files

    def set_rename_files(self, _rename_files: bool = False):
        self._rename_files = _rename_files

    def __init__(self, _is_zipped_file: bool = False,
                 _rename_files: bool = False) -> None:
        self._is_zipped_file = _is_zipped_file
        self.set_callback(Callback())
        self._rename_files = _rename_files

    def classify(self, path: str, output_path: str, file_filter: str):

        etree.set_default_parser(CustomElement.get_tree_parser())

        if '.zip' in file_filter:
            self.file_reader.read_zipped_files(True)
            self.file_reader._zip_filter = '*.xml'

            def execute(file, zip_file):
                self.__classify_zipped_invoices(file, zip_file, output_path)

        else:

            def execute(file):
                self.__classify_invoices(file, output_path)

        execute = getattr(self.callback, 'function', execute)
        self.callback.set_function(execute)

        self.file_reader.set_file_filter(file_filter)
        self.file_reader.do_in_list(path, self.callback)

        logger.info(f"Number of processed files: {len(self.callback.result)}")

        if(self.callback.errors and len(self.callback.errors) > 0):
            logger.info(
                f"Warnings or errors detected {len(self.callback.errors) }")
            for err in self.callback.errors:
                logger.error(err)

    def __classify_invoices(self, file: Path, output_path: str):

        tree: ElementTree = etree.parse(str(file))
        invoice: Comprobante = self.invoice_parser.parse(file.name, tree)

        new_output_path = self.__build_invoice_output_dir(invoice, output_path)

        # Copy file to output dir
        if self._rename_files:
            output_file = os.path.join(
                new_output_path, f"{invoice.tfd.uuid}.xml")
            shutil.copy(str(file), output_file)
        else:
            output_file = os.path.join(new_output_path, file.name)
            shutil.copy(str(file), new_output_path)

        logger.info('Copied file to: %s ' % (output_file))

        self.callback.result.append(output_file)

    def __classify_zipped_invoices(
            self, file: Path, zip_file: zipfile.ZipFile, output_path: str):

        with zip_file.open(file) as content_file:
            tree = etree.parse(content_file)
            invoice: Comprobante = self.invoice_parser.parse(file, tree)

        new_output_path = self.__build_invoice_output_dir(invoice, output_path)

        if self._rename_files:
            output_file = os.path.join(
                new_output_path, f"{invoice.tfd.uuid}.xml")
            self.__extract_file_with_new_name(file, zip_file, output_file)
        else:
            output_file = os.path.join(new_output_path, file)
            self.__extract_file_original_name(file, zip_file, new_output_path)

        logger.info(f'Extracted file to: {output_file}')

        # Add to callback result
        self.callback.result.append(output_file)

    def __build_invoice_output_dir(
            self, invoice: Comprobante, output_path: str) -> Path:
        # Build output dir name
        match = re.search(self.__DATE_PATTERN, invoice.doc_date)
        year = match.group(1)
        new_ouput_path = Path(
            os.path.join(
                output_path,
                year,
                invoice.issuer.rfc))
        new_ouput_path.mkdir(parents=True, exist_ok=True)

        return new_ouput_path

    def __extract_file_with_new_name(
            self, file: Path, zip_file: zipfile.ZipFile, output_file_name: str):
        # Extract the file with the new name
        with zip_file.open(file) as source, open(output_file_name, 'wb') as target:
            target.write(source.read())

    def __extract_file_original_name(
            self, file: Path, zip_file: zipfile.ZipFile, output_path: str):
        # Extract file to output dir
        zip_file.extract(file, output_path)
