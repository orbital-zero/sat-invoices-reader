#!/usr/bin/env python3

from xml.dom import NotFoundErr
from classes.dto.Comprobante import Comprobante, Issuer, TimbreFiscalDigital
from classes.parser.CustomElement import CustomElement
from classes.parser.InvoiceParserInterface import InvoiceParserInterface
from lxml.etree import _ElementTree as ET


class GeneralInvoiceParser(InvoiceParserInterface):

    def parse(self, file_name, file: ET) -> Comprobante:

        root: CustomElement = file.find('.')

        cfdi = Comprobante()

        if root is not None and 'comprobante' in root.tag.lower():
            root.setNamespaces(cfdi._ns)
        else:
            raise NotFoundErr('%s is not a valid xml invoice' % file_name)

        cfdi.setDate(root.get('fecha'))

        _type = root.get('tipodecomprobante')
        if(_type is not None):
            cfdi.setType(_type)

        _issuer = root.getElement('emisor')

        if _issuer is not None:
            issuer = Issuer()
            issuer.setRfc(_issuer.get('rfc'))
            cfdi.setIssuer(issuer)

        _tfd = root.getElement('complemento/timbrefiscaldigital')
        if _tfd is not None:
            uuid = _tfd.get('uuid')
            cfdi.setTfd(TimbreFiscalDigital(uuid))

        return cfdi
