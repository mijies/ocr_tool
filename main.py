from settings import *
from syuushi import Syuushi


syu = Syuushi()
# syu = Syuushi(DATA_DIR) # Specify directory if images are on local

print('\n Fetching images...\n')
try:
    syu.wget_src_imgs(BASE_URL, IMG_ITER(START_IMG_INDEX, end=FINAL_IMG_INDEX))
except NameError:
    syu.wget_src_imgs(BASE_URL, IMG_ITER(START_IMG_INDEX))
    
syu.print_img_list()
print('\n ...Done\n')

print('\n Performing OCR...')
syu.ocr_src_imgs()
print(' ...Done\n')

print('\n Creating report...')
syu.create_report()
print(' ...Done\n')

