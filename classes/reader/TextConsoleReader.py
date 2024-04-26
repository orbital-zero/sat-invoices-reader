#!/usr/bin/env python3

from typing import List
from xml.dom import NotSupportedErr
from classes.dto.Comprobante import Comprobante
from classes.parser.CustomElement import CustomElement
from classes.parser.InvoiceParserInterface import InvoiceParserInterface
from classes.dto.InvoiceType import InvoiceType
from classes.reader.InvoiceFileReader import InvoiceFileReader
from lxml import etree

import zipfile
import io
import typing


class TextConsoleReader:

    __PAYROLL_HEADER = ['archivo',
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
            'saldoNeto']
    
    __DEDUCTION_HEADER = ['archivo',
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
            'saldoNeto']

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
        return self._calback_res

    def read(self, path: str, _type: str):

        invoice_type = InvoiceType(_type)
        
        if invoice_type is InvoiceType.DEDUCTION:
            self.read_invoices(path, self.__DEDUCTION_HEADER, self.deductionParser, self.__print_deduction_record)
            #self.read_deductions(path)
        elif invoice_type == InvoiceType.PAYROLL:
            #self.read_payroll(path)
            self.read_invoices(path, self.__PAYROLL_HEADER, self.payrollParser, self.__print_payroll_record)
        else:
            raise NotSupportedErr('Invoce type not supported %(name)s' % _type)

    def read_invoices(self, path: str
                      , _headers: List
                      , invoice_parser: InvoiceParserInterface
                      , print_record: typing.Callable):
        
        print(*_headers, sep='|')
        
        callback = None
        self._calback_res = []
        xpath_parser = self.__get_tree_parser()

        if self.file_reader.is_zipped_file:
            # read invoices from zipped file
            callback = lambda filename, zip_file: self.__get_invoice_from_zip(
                filename,
                xpath_parser,
                zip_file,
                invoice_parser,
                print_record)

        else:
            # read invoices from file system
            callback = lambda filename: self.__get_invoice_from_file(
                filename,
                xpath_parser,
                invoice_parser,
                print_record)

        self._file_reader.do_in_list(path, callback)

    def __get_invoice_from_zip(self, filename: str
                        , custom_parser: etree.XMLParser
                        , zip_file: zipfile.ZipFile
                        , invoice_parser: InvoiceParserInterface
                        , print_record: typing.Callable) -> List:
        
        content = io.BytesIO(zip_file.read(filename))
        content_decoded = content.getvalue().decode('utf-8', 'ignore')
        
        if content_decoded.startswith('<?xml'):
            content_without_declaration = content_decoded.split('\n', 1)[1]
        else:
            content_without_declaration = content_decoded

        file = etree.fromstring(content_without_declaration, custom_parser)
        invoice = invoice_parser.parse(filename, file)
        
        if invoice is not None:
            print_record(invoice)
            self.callback_result.append(filename)

   
    def __get_invoice_from_file(self, filename: str
                     , custom_parser: etree.XMLParser
                     , invoice_parser: InvoiceParserInterface
                     , print_record: typing.Callable) -> List:
        
        file = etree.parse(filename, custom_parser)
        invoice = invoice_parser.parse(filename, file)

        if invoice is not None:
            print_record(invoice)
            self.callback_result.append(filename)


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

    def __get_tree_parser(self) -> etree.XMLParser:
        parser_lookup = etree.ElementDefaultClassLookup(element=CustomElement)
        parser = etree.XMLParser(recover= True)
        parser.set_element_class_lookup(parser_lookup)

        return parser
