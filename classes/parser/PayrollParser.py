#!/usr/bin/env python3

from classes.dto.Comprobante import Comprobante, Concept, Issuer, Payroll, TimbreFiscalDigital
from classes.parser.CustomElement import CustomElement
from classes.parser.InvoiceParserInterface import InvoiceParserInterface
from lxml.etree import _ElementTree as ET


class PayrollParser(InvoiceParserInterface):

    def __init__(self) -> None:
        self._readed_invoices = []

    @property
    def readed_invoices(self) -> list:
        return self._readed_invoices

    def clean_readed_invoices(self):
        self._readed_invoices = []

    def parse(self, file_name, file: ET) -> Comprobante:

        cfdi = Comprobante()

        root: CustomElement = file.find('.')
        root.setNamespaces(cfdi._ns)

        _type = root.get('tipodecomprobante')
        if(_type is not None and _type != 'N'):
            return

        _tfd = root.getElement('complemento/timbrefiscaldigital')
        if _tfd is not None:
            uuid = _tfd.get('uuid')
            if uuid in self.readed_invoices:
                raise ValueError(
                    "duplicated uuid %s in %s" %
                    (uuid, file_name))
            else:
                self.readed_invoices.append(uuid)
                cfdi.setTfd(TimbreFiscalDigital(uuid))

        cfdi.setFilename(file_name)
        cfdi.setType(_type)
        cfdi.setVersion(root.get('version'))
        cfdi.setDate(root.get('fecha'))
        cfdi.setSubtotal(root.get('subtotal'))
        cfdi.setTotal(root.get('total'))

        _issuer = root.getElement('emisor')

        if _issuer is not None:
            issuer = Issuer()
            issuer.setName(_issuer.get('nombre'))
            issuer.setRfc(_issuer.get('rfc'))
            cfdi.setIssuer(issuer)

        _concept = root.getElement('conceptos/concepto')

        if(_concept is not None and isinstance(_concept, list)):
            cfdi.setConcepts([Concept(_concept[0].get('descripcion'))])
        else:
            cfdi.setConcepts([Concept(_concept.get('descripcion'))])

        _payroll = root.getElement('complemento/nomina')

        if _payroll is not None:
            payroll = Payroll()
            payroll.setStartPaymentDate(_payroll.get('fechainicialpago'))
            payroll.setEndPaymentDate(_payroll.get('fechafinalpago'))

            _deductions = root.getElement(
                'complemento/nomina/deducciones/deduccion')

            cfdi.setPayroll(payroll)
            self.assing_deductions(_deductions, cfdi)

        return cfdi

    def get_paid_tax_deduction(self, _deduc):
        if _deduc.get('tipodeduccion') == '002':
            return _deduc.get('importe') or _deduc.get('importegravado')

    def assing_deductions(self, _deductions, cfdi):
        if isinstance(_deductions, list):

            for _deduc in _deductions:
                paidTax = self.get_paid_tax_deduction(_deduc)
                if paidTax is not None:
                    cfdi.payroll.setPaidTax(paidTax)

        elif _deductions is not None:
            cfdi.payroll.setPaidTax(self.get_paid_tax_deduction(_deductions))
