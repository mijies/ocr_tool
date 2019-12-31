
# Define image source constants
BASE_URL = 'http://www.kokuseikyo.or.jp/syuushi/img/29/'
IMG_EXTENSION = 'png'

START_IMG_INDEX = 1
FINAL_IMG_INDEX = 2 # comment out for all the images after START_IMG_INDEX

def IMG_ITER(n, end=None): # generator to return image file names
    stop_func = (lambda x: True) if end is None else (lambda x: x <= end)
    while stop_func(n):
        yield '{:0>2}.{}'.format(n, IMG_EXTENSION)
        n += 1

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
ASYNC_PARALLEL_LIMIT = 5

# Define multi process execution constatnts
import multiprocessing
PROC_PARALLEL_LIMIT = multiprocessing.cpu_count() # upto the number of CPU cores