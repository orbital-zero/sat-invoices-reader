#!/usr/bin/env python3

import sys
import argparse
import logging
import logging.config

from classes.manager.InvoiceClassifier import InvoiceClassifier
from classes.parser.GeneralInvoiceParser import GeneralInvoiceParser
from classes.reader.CustomizableFileReader import CustomizableFileReader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        # logging.FileHandler('classify.log')
    ]
)
logger = logging.getLogger(__name__)

_epilog = '''
These are an examples to execute the command:

    # sort xml files by invoice year and issuer from source directory, then leave it in another directory
        ./classify.py -p <sourcesPath> -o <targetPath>

    # sort xml files by invoice year and issuer from source directory, then leave it in another directory changing names by uuid value
        ./classify.py -p <sourcesPath> -o <targetPath> -u

    # extract and sort xml zipped files from a directory and leave it in another one
        ./classify.py -p <sourcesPath> -o <targetPath> -x

    # extract and sort xml zipped files from a directory and leave it in another one changing their names by uuid value
        ./classify.py -p <sourcesPath> -o <targetPath> -xu
'''


def main(argv):

    parser = argparse.ArgumentParser(description='Classify invoices by issuer and year of creation',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, epilog=_epilog)
    parser.add_argument('-p', '--sourcesPath', required=True, type=str, metavar="source_path",
                        help='source directory to read xml files')
    parser.add_argument('-o', '--targetPath', required=True, type=str, metavar='target_path',
                        help='target directory to put sorted xml files')
    parser.add_argument('-x', '--extract', action='store_true', help='Extract xml from zipped files to sort.')
    parser.add_argument('-u', '--uuid_names', action='store_true', help='The output file will be renamed by their invoice uuid')

    args = parser.parse_args()

    manager = InvoiceClassifier()
    manager.set_invoice_parser(GeneralInvoiceParser())
    manager.set_rename_files(args.uuid_names)

    file_reader = CustomizableFileReader(args.extract, True)
    filter = '**/*.zip' if (args.extract) else '**/*.xml'

    manager.set_file_reader(file_reader)

    logger.info("Starting invoice classification process...")
    manager.classify(args.sourcesPath, args.targetPath, filter)

if __name__ == "__main__":
    main(sys.argv[1:])
