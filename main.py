#!/usr/bin/env python3

import sys
import argparse
import logging
import logging.config

from classes.parser.DeductionsParser import DeductionsParser
from classes.parser.PayrollParser import PayrollParser
from classes.reader.CustomizableFileReader import CustomizableFileReader
from classes.reader.InvoiceReader import InvoiceReader
from classes.reader.TextConsoleReader import TextConsoleReader

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
These are an examples to execute the command:\n
    # read xml files from directory
    \t./main.py -p <sourcesPath>

    # read zipped xml files from directory
    \t./main.py -p <sourcesPath> -x

    # read zipped xml files from directory using encoding 'iso-8859-1'
    \t./main.py -p <sourcesPath> -e iso-8859-1 -x
'''


def main(argv):

    parser = argparse.ArgumentParser(
                                    description='Process to read invoces from a specified directory (xml or zipped files)',
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    epilog=_epilog)
    parser.add_argument('-p', '--sourcesPath', required=True, type=str, metavar="path",
                        help='Path to directory, the nestted directories are included in the processing.')
    parser.add_argument('-t', '--type', type=str, nargs='?', metavar='P,D', default='P',
                        help='Invoice type, P for payroll (by default) or D for deductions.')
    parser.add_argument('-x', '--extract', action='store_true', help='Extract xml from zipped files.')
    # parser.add_argument('-e','--encoding', metavar='fileEncoding', type=str, default='utf-8'
    #                    , help=''' Set file encoding to read files, by default 'utf-8' ''')

    args = parser.parse_args()

    invoce_reader = InvoiceReader()
    invoce_reader.set_deductuction_parser(DeductionsParser())
    invoce_reader.set_payroll_parser(PayrollParser())
    
    invoce_reader.set_file_reader(CustomizableFileReader(args.extract, False))
    
    logger.info("Starting invoice read process...")
    
    console = TextConsoleReader(invoce_reader)
    console.read(args.sourcesPath, args.type)


if __name__ == "__main__":
    main(sys.argv[1:])