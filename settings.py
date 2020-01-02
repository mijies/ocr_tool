
# Define image source constants
BASE_URL = 'http://www.kokuseikyo.or.jp/syuushi/img/29/'
IMG_EXTENSION = 'png'

START_IMG_INDEX = 1
FINAL_IMG_INDEX = 25 # required when WGET_ASYNC is True or comment out for all the images after START_IMG_INDEX

def IMG_ITER(idx, end=None): # generator to return image file names
    stop_func = (lambda x: True) if end is None else (lambda x: x <= end)
    while stop_func(idx):
        yield '{:0>2}.{}'.format(idx, IMG_EXTENSION)
        idx += 1


# Define data directory constants
DATA_DIR = 'data_'
import datetime
DATA_DIR = 'data_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S")


# Define ocr constants
OCR_LANG = 'jpn'
OCR_FILE_EXTENSION = 'txt'


# Define constants for preprocess before ORC
DPI_CONVERT = True      # adjust image dpi
DPI_TUPLE = (300, 300)  # required when DPI_CONVERT is True, dpi value (int, int)
SPLIT_VERTICAL = True   # split image vertically


# Define report constants
REPORT_FILE_PREFIX = 'syuushi_'
REPORT_FILE_EXTENSION = 'xlsx'
REPORT_COLUMN_SPAN = 2


# Define asynchronous IO constatnts
WGET_ASYNC = True
ASYNC_PARALLEL_LIMIT = 5


# Define multi process execution constatnts
OCR_PARALLEL = True
import multiprocessing
PROC_PARALLEL_LIMIT = multiprocessing.cpu_count() - 1 # one short of the number of CPU cores


## Do NOT edit below

if WGET_ASYNC:
    try:
        if FINAL_IMG_INDEX <= START_IMG_INDEX:
            exit(1)
    except:
        print('\n FINAL_IMG_INDEX must be properly set when WGET_ASYNC is True')
        exit(1)


IMG_ITER_KWARGS = {}
IMG_ITER_KWARGS['idx'] = START_IMG_INDEX
try:
    IMG_ITER_KWARGS['end'] = FINAL_IMG_INDEX
except: pass

if DPI_CONVERT:
    try:
        if type(DPI_TUPLE) is not type(()):
            exit(1)
    except:
        print('\n DPI_TUPLE must be set as tuple class when DPI_CONVERT is True')
        exit(1)

# Argument to pass Shyuushi Initializer
SYUUSHI_KWARGS = {}
SYUUSHI_KWARGS['data_dir'] = DATA_DIR
SYUUSHI_KWARGS['wget_async'] = WGET_ASYNC
SYUUSHI_KWARGS['ocr_parallel'] = OCR_PARALLEL

if WGET_ASYNC:
    print('\n Image downloading in asynchronous IO mode')
if OCR_PARALLEL:
    print(' Image OCR in multi-processor mode\n')


