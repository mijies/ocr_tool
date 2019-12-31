
# Define image source constants
BASE_URL = 'http://www.kokuseikyo.or.jp/syuushi/img/29/'
IMG_EXTENSION = 'png'

START_IMG_INDEX = 1
FINAL_IMG_INDEX = 2

def IMG_ITER(idx, end=None): # generator to return image file names
    stop_func = (lambda x: True) if end is None else (lambda x: x <= end)
    while stop_func(idx):
        yield '{:0>2}.{}'.format(idx, IMG_EXTENSION)
        idx += 1

IMG_ITER_KWARGS = {}
IMG_ITER_KWARGS['idx'] = START_IMG_INDEX
IMG_ITER_KWARGS['end'] = FINAL_IMG_INDEX # comment out for all the images after START_IMG_INDEX


# Define data directory constants
DATA_DIR = 'data_'


# Define ocr constants
OCR_LANG = 'jpn'
OCR_FILE_EXTENSION = 'txt'


# Define report constants
REPORT_FILE_PREFIX = 'syuushi_'
REPORT_FILE_EXTENSION = 'xlsx'
REPORT_COLUMN_SPAN = 2


# Define asynchronous IO constatnts
IS_ASYNC = False
ASYNC_PARALLEL_LIMIT = 5


# Define multi process execution constatnts
OCR_PARALLEL = False
REP_PARALLEL = False
import multiprocessing
PROC_PARALLEL_LIMIT = multiprocessing.cpu_count() - 1 # one short of the number of CPU cores


# Argument to pass Shyuushi Initializer
SYUUSHI_KWARGS = {}
SYUUSHI_KWARGS['data_dir'] = DATA_DIR
SYUUSHI_KWARGS['is_async'] = IS_ASYNC
SYUUSHI_KWARGS['ocr_parallel'] = OCR_PARALLEL

