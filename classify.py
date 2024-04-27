#!/usr/bin/env python3

import sys
import argparse
from classes.manager.InvoiceClassifier import InvoiceClassifier
from classes.parser.GeneralInvoiceParser import GeneralInvoiceParser
from classes.reader.CustomizableFileReader import CustomizableFileReader

_epilog = '''
These are an examples to execute the command:

    # sort xml files from a directory
    \t./classify.py -p <sourcesPath> -o <targetPath>

    # extract and sort xml zipped files from a directory
    \t./classify.py -p <sourcesPath> -o <targetPath> -z
'''


def main(argv):

    parser = argparse.ArgumentParser(description='Classify invoices by issuer and year of creation',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, epilog=_epilog)
    parser.add_argument('-p', '--sourcesPath', required=True, type=str, metavar="source_path",
                        help='source directory to read xml files')
    parser.add_argument('-o', '--targetPath', required=True, type=str, metavar='target_path',
                        help='target directory to put sorted xml files')
    parser.add_argument('-x', '--extract', action='store_true', help='Extract xml from zipped files to sort.')

    args = parser.parse_args()

    manager = InvoiceClassifier()
    manager.set_invoice_parser(GeneralInvoiceParser())

    if(args.extract):
        manager.set_file_reader(CustomizableFileReader(True, True))
        filter = '**/*.zip'
    else:
        manager.set_file_reader(CustomizableFileReader(False, True))
        filter = '**/*.xml'

    manager.classify(args.sourcesPath, args.targetPath, filter)


if __name__ == "__main__":
    main(sys.argv[1:])
