
# Define image source constants
BASE_URL = 'http://www.kokuseikyo.or.jp/syuushi/img/29/'
IMG_EXTENSION = 'png'

def IMG_ITER(n): # generator to return image file names
    while True:
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