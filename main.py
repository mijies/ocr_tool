from settings import *
from syuushi import Syuushi
import time

# syu = Syuushi()
# syu = Syuushi(is_async=True) # asynchronously execute
syu = Syuushi(DATA_DIR) # Specify directory if images are on local

start_time = time.time()
print('\n Fetching images...\n')
try:
    syu.wget_src_imgs(BASE_URL, IMG_ITER(START_IMG_INDEX, end=FINAL_IMG_INDEX))
except NameError:
    syu.wget_src_imgs(BASE_URL, IMG_ITER(START_IMG_INDEX))

print('\n ...Done')
print('\n Time: ', time.time() - start_time)

start_time = time.time()
print('\n Performing OCR...\n')
syu.ocr_src_imgs()
print('\n ...Done\n')
print(' List of OCRed files\n')
syu.print_ocr_list()
print('\n Time: ', time.time() - start_time)

start_time = time.time()
print('\n Creating report...\n')
syu.create_report()
print('\n ...Done\n')
print('\n Time: ', time.time() - start_time)

