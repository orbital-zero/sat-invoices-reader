#!/usr/bin/env python3

from pathlib import Path
from xml.etree.ElementTree import ElementTree
from classes.dto.Comprobante import Comprobante
from classes.parser.CustomElement import CustomElement
from classes.parser.InvoiceParserInterface import InvoiceParserInterface
from classes.reader.Callback import Callback
from classes.reader.FileReaderInterface import FileReaderInterface
from lxml import etree

import io
import re
import shutil
import logging
import zipfile
import os

logger = logging.getLogger(__name__)


class InvoiceClassifier:

    __DATE_PATTERN = r"(\d{4})[/.-](\d{2})[/.-](\d{2})"

    def __init__(self, _is_zipped_file: bool = False) -> None:
        self._is_zipped_file = _is_zipped_file

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
    def callback_errors(self) -> dict:
        return self.callback.errors

    @property
    def callback_result(self) -> dict:
        return self.callback.result

    def classify(self, path: str, target: str, filter: str):

        custom_parser = CustomElement.get_tree_parser()

        if '.zip' in filter:
            self.file_reader.read_zipped_files(True)

            def execute(file, zip_file):
                self.__classify_zipped_invoices(file, zip_file, custom_parser, target)
        else:
            def execute(file):
                self.__classify_invoices(file, custom_parser, target)

        self.callback = Callback()
        self.callback.set_function(execute)
        self.file_reader.do_in_list(path, self.callback, filter)

    def __classify_invoices(self, file: Path, parser: etree.XMLParser, target: str):

        tree: ElementTree = etree.parse(file, parser)
        invoice: Comprobante = self.invoice_parser.parse(file.name, tree)

        output_path = self.__get_ouput_path(invoice, target)
        output_path.mkdir(parents=True, exist_ok=True)

        new_name = invoice.tfd.uuid + ".xml"
        dest = self.__get_destination(output_path, new_name)

        shutil.copy(str(file), dest)

        self.callback.result.append(dest)

    def __classify_zipped_invoices(self, file: Path, zip_file: zipfile.ZipFile,
                                   parser: etree.XMLParser, target: str):

        content = io.BytesIO(zip_file.read(file))
        contentDecoded = content.getvalue().decode('utf-8', 'ignore')
        tree = etree.fromstring(contentDecoded, parser)
        invoice: Comprobante = self.invoice_parser.parse(file, tree)

        output_path = self.__get_ouput_path(invoice, target)
        output_path.mkdir(parents=True, exist_ok=True)

        zip_info = zip_file.getinfo(file)
        zip_info.filename = invoice.tfd.uuid + ".xml"
        dest = self.__get_destination(output_path, zip_info.filename)

        zip_file.extract(zip_info, output_path)

        self.callback.result.append(dest)

    def __get_ouput_path(self, invoice: Comprobante, target) -> Path:
        match = re.search(self.__DATE_PATTERN, invoice.doc_date)
        year = match.group(1)

        return Path(os.path.join(target, year, invoice.issuer.rfc))

    def __get_destination(self, output_path: str, filename: str) -> str:
        dest = os.path.join(output_path, filename)
        logger.debug('copying file to: %s ' % (dest))
        return dest
