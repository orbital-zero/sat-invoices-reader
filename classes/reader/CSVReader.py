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


class CSVReader:

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
        
        entries = []
                
        if _type == 'D':
            
            def read_invoice(invoice: Comprobante):
                """" custom function to read each deduction invoce """
                if invoice is not None:
                    entries.append(self.__get_deduction_record(invoice))
            
            self.__read_files_to_csv(path, self.deductionParser, read_invoice, entries )

        elif _type == 'P':
            
            def read_invoice(invoice: Comprobante):
                """" custom function to read each payroll invoice """
                if invoice is not None:
                    entries.append(self.__get_payroll_record(invoice))

            self.__read_files_to_csv(path, self.payrollParser, read_invoice, entries)
            

        else:
            raise NotSupportedErr('Invoce type not supported %s' % _type)



    def conact_pipes(self, entries: list) -> list:
        """ Concatenate a pipe char '|' with each entry of the list """
        return ["|".join(w) + "" for w in entries] 

    def __read_files_to_csv(self, path: str, invoice_parser: InvoiceParserInterface, read_invoice, entries):

        headers = ['archivo', 'xml version', 'cfdiUuid', 'fecha','descripcion',
            'fechainicialpago','fechafinalpago','nombre emisor', 'rfc emisor',
            'totalGravado', 'impuestoRetenido','saldoNeto']
        
        entries.append(headers)

        self.callback = Callback()
        self.__read_invoices(path, CustomElement.get_tree_parser(), invoice_parser, read_invoice)
        self.callback.result.append(self.conact_pipes(entries))
        

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

    def __get_deduction_record(self, invoice: Comprobante):
        
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
        tree = etree.fromstring(content_decoded, tree_parser)
        return invoice_parser.parse(file, tree)

    def __get_invoice_from_file(self, file: str, tree_parser: etree.XMLParser,
                                invoice_parser: InvoiceParserInterface) -> Comprobante:
        """Get an invoice file from file system, requires a parser to convert invoice"""

        tree = etree.parse(file, tree_parser)
        return invoice_parser.parse(str(file), tree)

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
