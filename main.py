from settings import *
from syuushi import Syuushi
import time

syu = Syuushi(**SYUUSHI_KWARGS)

if __name__ == '__main__':

    start_time = time.time()
    print('\n Fetching images...\n')
    syu.wget_src_imgs(BASE_URL, IMG_ITER(**IMG_ITER_KWARGS))
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



