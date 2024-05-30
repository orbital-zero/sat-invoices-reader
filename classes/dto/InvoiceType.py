#!/usr/bin/env python3

from enum import Enum


class InvoiceType(Enum):
    PAYROLL = 'P'
    DEDUCTION = 'D'
    RETENTION = 'R'
