import eel, os, random
import logging
import webview, threading

from tkinter import filedialog
from tkinter import *

from classes.parser.DeductionsParser import DeductionsParser
from classes.parser.PayrollParser import PayrollParser
from classes.reader.CSVReader import CSVReader
from classes.reader.InvoiceFileReader import InvoiceFileReader
from classes.manager.InvoiceClassifier import InvoiceClassifier
from classes.parser.GeneralInvoiceParser import GeneralInvoiceParser

logger = logging.getLogger(__name__)  

# Set web files folder
eel.init('web')

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)
    

say_hello_py('Python World!')
eel.say_hello_js('Python World!')   # Call a Javascript function



@eel.expose
def pick_file(folder):
    if os.path.isdir(folder):
        return random.choice(os.listdir(folder))
    else:
        return 'Not valid folder'


@eel.expose
def btn_dir_path():
	root = Tk()
	root.withdraw()
	root.wm_attributes('-topmost', 1)
	folder = filedialog.askdirectory()
	return folder

@eel.expose
def dialog_save_csv():
	root = Tk()
	root.withdraw()
	root.wm_attributes('-topmost', 1)

	file = filedialog.asksaveasfilename(filetypes = (("CSV files","*.csv"),("all files","*.*")),
     defaultextension = (("CSV files","*.csv")))
    # file =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("CSV files","*.csv"),("all files","*.*")))

	return file

@eel.expose
def read_invoices(folder, zip:bool, type):

    # logger.error("path:{0} zip:{1} type:{2} ".format(folder,zip, type))
    reader = CSVReader()
    reader.setDeductuctionParser(DeductionsParser())
    reader.setPayrollParser(PayrollParser())
    reader.setFileReader(InvoiceFileReader())

    if type is None:
        type = 'P'

    if zip is None:
        reader.file_reader.read_zipped_files(False)
    else:
        reader.file_reader.read_zipped_files(zip)

    reader.read(folder, type)

    data = { 'result': reader.callback.result[0],
             'errors': __to_str_list(reader.callback.errors) }

    return  data;

def __to_str_list(data) -> list:
    """ Convert a list entries to str list """
    entries = []
    for e in data:
        entries.append(str(e))
    return entries

@eel.expose
def save_text_file(output, content):
    """" write a csv file """
    with open(output, 'w') as f:
        f.write(content)

@eel.expose
def classify_invoices(source, target, zip:bool):
    manager = InvoiceClassifier()
    manager.set_invoice_parser(GeneralInvoiceParser())

    if(zip):
        manager.set_file_reader(InvoiceFileReader(True, True))
        filter = '**/*.zip'
    else:
        manager.set_file_reader(InvoiceFileReader(False, True))
        filter = '**/*.xml'
    
    manager.classify(source, target, filter)

    data = { 'result': manager.callback_result,
             'errors': manager.callback_errors }

    return data


def start_app():
    eel_thread = threading.Thread(target=eel_start) # Eel app start.
    eel_thread.daemon = True
    eel_thread.start() # Run eel in a seperate thread.

    webview_start() # Start pywebview web browser.

def eel_start():
    # EEL app start.
    eel.init('web')
    eel.start('file_access.html', size=(800, 600), mode=None)

def webview_start():
    # pywebview start.
    # https://pywebview.flowrl.com/guide/api.html#webview-create-window
    webview.create_window('SAT Invoice Reader',
     'http://localhost:8000/index.html',
     frameless=True)
    webview.start(gui='qt')

start_app()