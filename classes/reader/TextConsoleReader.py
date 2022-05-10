#!/usr/bin/env python3

from xml.dom import NotSupportedErr
from classes.reader.Callback import Callback
from classes.dto.Comprobante import Comprobante
from classes.parser.CustomElement import CustomElement
from classes.parser.InvoiceParserInterface import InvoiceParserInterface
from classes.reader.InvoiceFileReader import InvoiceFileReader
from lxml import etree

import zipfile
import io


class TextConsoleReader:

    @property
    def deductionParser(self) -> InvoiceParserInterface:
        return self._deduct_parser

    def setDeductuctionParser(self, _deduct_parser: InvoiceParserInterface):
        self._deduct_parser = _deduct_parser

    @property
    def payrollParser(self) -> InvoiceParserInterface:
        return self._payroll_parser

    def setPayrollParser(self, _payroll_parser: InvoiceParserInterface):
        self._payroll_parser = _payroll_parser

    @property
    def file_reader(self) -> InvoiceFileReader:
        return self._file_reader

    def setFileReader(self, _reader: InvoiceFileReader):
        self._file_reader = _reader

    @property
    def callback_result(self) -> dict:
        return self.callback.result

    def read(self, path: str, _type: str):

        if _type == 'D':
            self.read_deductions(path)
        elif _type == 'P':
            self.read_payroll(path)
        else:
            raise NotSupportedErr('Invoce type not supported %s' % _type)

    def read_payroll(self, path: str):

        print(
            'archivo',
            'xml version',
            'cfdiUuid',
            'fecha',
            'descripcion',
            'fechainicialpago',
            'fechafinalpago',
            'nombre emisor',
            'rfc emisor',
            'totalGravado',
            'impuestoRetenido',
            'saldoNeto',
            sep='|')

        self.callback = Callback()
        tree_parser = CustomElement.get_tree_parser()

        def read_invoice(invoice: Comprobante):
            """" custom action to read payroll invoices """
            if invoice is not None:
                self.__print_payroll_record(invoice)
                self.callback.result.append(invoice.tfd.uuid)

        self.__read_invoices(path, tree_parser, self.payrollParser, read_invoice)

    def read_deductions(self, path: str):

        print(
            'archivo',
            'xml version',
            'cfdiUuid',
            'fecha',
            'descripcion',
            'fechainicialpago',
            'fechafinalpago',
            'nombre emisor',
            'rfc emisor',
            'totalGravado',
            'impuestoRetenido',
            'saldoNeto',
            sep='|')

        self.callback = Callback()
        tree_parser = CustomElement.get_tree_parser()

        def read_invoice(invoice: Comprobante):
            """" custom action to read deduction invoices """
            self.__print_deduction_record(invoice)
            self.callback.result.append(invoice.tfd.uuid)

        self.__read_invoices(path, tree_parser, self.deductionParser, read_invoice)

    def __print_payroll_record(self, invoice: Comprobante):
        print(
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
            invoice.total,
            sep='|')

    def __print_deduction_record(self, invoice: Comprobante):
        print(
            invoice.file_name,
            invoice.version,
            invoice.tfd.uuid,
            invoice.doc_date,
            invoice.concepts[0].description,
            invoice.issuer.name,
            invoice.issuer.rfc,
            invoice.subtotal,
            invoice.total,
            sep='|')

    def __get_invoice_from_zip(self, file: str, tree_parser: etree.XMLParser,
                               zip_file: zipfile.ZipFile,
                               invoice_parser: InvoiceParserInterface) -> Comprobante:
        """Get an invoice file from zip file, requires a parser to convert invoice"""

        content = io.BytesIO(zip_file.read(file))
        content_decoded = content.getvalue().decode('utf-8', 'ignore')
        tree = etree.fromstring(content_decoded, tree_parser)
        return invoice_parser.parse(file, tree)

    def __get_invoice_from_file(self, file: str, tree_parser: etree.XMLParser,
                                invoice_parser: InvoiceParserInterface) -> Comprobante:
        """Get an invoice file from file system, requires a parser to convert invoice"""

        tree = etree.parse(file, tree_parser)
        return invoice_parser.parse(file, tree)

    def __read_invoices(self, path: str, tree_parser, invoice_parser: InvoiceParserInterface, read_invoice):
        """Read invoices from xml or zipped files passing a cusmoziable function when file is readed,
            an invoice parser is required to convert invoice"""

        if self.file_reader.is_zipped_file:
            # read xml from zip file
            def invoice_func(filename, zip_file):
                invoice = self.__get_invoice_from_zip(filename, tree_parser, zip_file, invoice_parser)
                read_invoice(invoice)

            file_filter = '**/*.zip'

        else:
            # read xml from file system
            def invoice_func(file):
                invoice = self.__get_invoice_from_file(file, tree_parser, invoice_parser)
                read_invoice(invoice)

            file_filter = '**/*.xml'

        self.callback.set_function(invoice_func)
        self._file_reader.do_in_list(path, self.callback, file_filter)
