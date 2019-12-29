from settings import *
from syuushi import Syuushi


syu = Syuushi(DATA_DIR)

syu.wget_src_imgs(BASE_URL, IMG_ITER(23))
print('\n Images fetched\n')
syu.print_img_list()

syu.ocr_src_imgs()
print('\n OCR completed')

syu.report_in_excel()
print('\n Report created')

