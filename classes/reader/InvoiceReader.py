#!/usr/bin/env python3

from xml.dom import NotSupportedErr
from classes.dto.Callback import Callback
from classes.dto.Comprobante import Comprobante
from classes.parser.CustomElement import CustomElement
from classes.parser.InvoiceParserInterface import InvoiceParserInterface
from classes.reader.CustomizableFileReader import CustomizableFileReader
from lxml import etree
from typing import Callable
import zipfile
import io


class InvoiceReader:

    __HEADERS = ['archivo', 'xml version', 'cfdiUuid', 'fecha', 'descripcion',
                 'fechainicialpago', 'fechafinalpago', 'nombre emisor', 'rfc emisor',
                 'totalGravado', 'impuestoRetenido', 'saldoNeto']

    @property
    def deduction_parser(self) -> InvoiceParserInterface:
        return self._deduct_parser

    def set_deductuction_parser(self, _deduct_parser: InvoiceParserInterface):
        self._deduct_parser = _deduct_parser

    @property
    def payroll_parser(self) -> InvoiceParserInterface:
        return self._payroll_parser

    def set_payroll_parser(self, _payroll_parser: InvoiceParserInterface):
        self._payroll_parser = _payroll_parser

    @property
    def file_reader(self) -> CustomizableFileReader:
        return self._file_reader

    def set_file_reader(self, _reader: CustomizableFileReader):
        self._file_reader = _reader

    @property
    def callback(self) -> Callback:
        return self._callback

    def set_callback(self, _callback: Callback):
        self._callback = _callback

    def __init__(self) -> None:
        self.set_callback(Callback())

    def read(self, path: str, _type: str):

        if _type == 'D':
            self._read_invoices(
                path,
                self.__get_deduction_record,
                self.deduction_parser)
        elif _type == 'P':
            self._read_invoices(
                path,
                self.__get_payroll_record,
                self.payroll_parser)
        else:
            raise NotSupportedErr('Invoce type not supported %s' % _type)

    def _read_invoices(
            self, path: str, _get_invoice_record: Callable, _invoice_parser: Callable):

        # add headers
        self.__add_header_to_result(self.__HEADERS)

        # Read invoce data
        self.__read_invoices_from_path(
            path,
            CustomElement.get_tree_parser(),
            _invoice_parser,
            lambda invoice: self.__add_invoice_to_result(invoice, _get_invoice_record)
        )
        # self.convert_to_csv(self.callback.result)

    def __add_header_to_result(self, headers: list):
        """" Custom function to add field output names to callback result"""
        self.callback.result.append(headers)

    def __add_invoice_to_result(
            self, invoice: Comprobante, _get_record: Callable):
        """" Custom function to add readed invoices to callback result"""
        if invoice is not None:
            self.callback.result.append(_get_record(invoice))

    def __get_payroll_record(self, invoice: Comprobante) -> list:

        return [
            invoice.file_name,
            invoice.version,
            invoice.tfd.uuid,
            invoice.doc_date,
            invoice.concepts[0].description,
            invoice.payroll.start_payment_date,
            invoice.payroll.end_payment_date,
            invoice.issuer.name,
            invoice.issuer.rfc,
            invoice.subtotal,
            invoice.payroll.paid_tax,
            invoice.total
        ]

    def __get_deduction_record(self, invoice: Comprobante) -> list:

        return [
            invoice.file_name,
            invoice.version,
            invoice.tfd.uuid,
            invoice.doc_date,
            invoice.concepts[0].description,
            invoice.issuer.name,
            invoice.issuer.rfc,
            invoice.subtotal,
            invoice.total,
        ]

    def __get_invoice_from_zip(self, file: str, tree_parser: etree.XMLParser,
                               zip_file: zipfile.ZipFile,
                               invoice_parser: InvoiceParserInterface) -> Comprobante:
        """Get an invoice file from zip file, requires a parser to convert invoice"""

        content = io.BytesIO(zip_file.read(file))
        content_decoded = content.getvalue().decode('utf-8', 'ignore')

        if content_decoded.startswith('<?xml'):
            content_without_declaration = content_decoded.split('\n', 1)[1]
        else:
            content_without_declaration = content_decoded

        tree = etree.fromstring(content_without_declaration, tree_parser)
        return invoice_parser.parse(file, tree)

    def __get_invoice_from_file(self, file: str, tree_parser: etree.XMLParser,
                                invoice_parser: InvoiceParserInterface) -> Comprobante:
        """Get an invoice file from file system, requires a parser to convert invoice"""

        tree = etree.parse(str(file), tree_parser)
        return invoice_parser.parse(str(file), tree)

    def __read_invoices_from_path(self, path: str, tree_parser,
                                  invoice_parser: InvoiceParserInterface, _callback: Callable):
        """Read invoices from xml or compressed files, the invoce parser is neded to conver xml to invoce object,
            also requiere a custom callback to retrieve or process the invoice data"""

        if self.file_reader.is_zipped_file:
            # read xml from zip file
            def reader_callback(filename, zip_file):
                invoice = self.__get_invoice_from_zip(
                    filename, tree_parser, zip_file, invoice_parser)
                _callback(invoice)

            file_filter = '**/*.zip'

        else:
            # read xml from file system
            def reader_callback(file):
                invoice = self.__get_invoice_from_file(
                    file, tree_parser, invoice_parser)
                _callback(invoice)

            file_filter = '**/*.xml'

        self.callback.set_function(reader_callback)
        self._file_reader.set_file_filter(file_filter)
        self._file_reader.do_in_list(path, self.callback)
