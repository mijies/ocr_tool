import asyncio
import concurrent.futures as parallel
import datetime
import glob
import io
import os
from PIL import Image
import pyocr
import pyocr.builders
import re
import requests

from settings import *
from excel import ExcelHandle, new_excel_handle

tool = pyocr.get_available_tools()[0]

class Syuushi:
    def __init__(self, data_dir=None, is_async=False, ocr_parallel=False):
        self.src_img_list = []
        self.ocr_txt_list = []

        if data_dir is None: # make new data directory
            self.data_dir = 'data_%s' % get_timestamp()
            os.makedirs(self.data_dir)
        else: # use pre-made data directory and source images
            self.data_dir = data_dir
            img_list = glob.glob(os.path.join(data_dir, '*.' + IMG_EXTENSION))
            self.src_img_list = [os.path.split(path)[-1] for path in img_list]

        self.is_async = is_async
        self.ocr_parallel = ocr_parallel
        
        if is_async:
            print('\n Image downloading in asynchronous IO mode')
        if ocr_parallel:
            print('\n Image OCR in multi-processor mode')


    def print_img_list(self):
        [print(' ', img) for img in self.src_img_list]

    def print_ocr_list(self):
        [print(' ', ocr) for ocr in self.ocr_txt_list]


    def wget_src_imgs(self, base_url, img_iter):
        if len(self.src_img_list) != 0:
            print(' ...Found on local\n')
            self.print_img_list()
            return

        if self.is_async:
            loop = asyncio.get_event_loop() 
            future = async_run(img_iter, wget_img, base_url, self.data_dir)
            self.src_img_list = loop.run_until_complete(future)
        else:
            self.src_img_list = [wget_img(img, base_url, self.data_dir) for img in img_iter]


    def ocr_src_imgs(self):
        timestamp = get_timestamp()
        if self.ocr_parallel:
            with parallel.ProcessPoolExecutor(max_workers=PROC_PARALLEL_LIMIT) as executor:
                futures = [executor.submit(ocr_imgs, img, self.data_dir, timestamp) for img in self.src_img_list]
                self.ocr_txt_list = [future.result() for future in parallel.as_completed(futures)]
        else:
            self.ocr_txt_list = [ocr_imgs(img, self.data_dir, timestamp) for img in self.src_img_list]
    

    def create_report(self):
        txt_list = open_read_file_list(self.data_dir, self.ocr_txt_list)
        report = '%s%s.%s' % (REPORT_FILE_PREFIX, get_timestamp(), REPORT_FILE_EXTENSION)
        path = os.path.join(self.data_dir, report)
        ex = new_excel_handle(path)
        report_in_excel(ex, self.src_img_list, txt_list)


def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def wget_img(img, base_url, data_dir):
    res = requests.get(base_url + img)
    if res.status_code != 200:
        return
    if 'image' not in res.headers['content-type']:
        print("Content-Type must be image\n URL: %s\n Content-Type: %s" % (img, content_type))
        exit(1)

    path = os.path.join(data_dir, img)
    with open(path, 'wb') as f:
        f.write(res.content)
    
    print(' ', img, 'fetched')
    return img


def ocr_imgs(img, data_dir, timestamp):
    path = os.path.join(data_dir, img)
    txt = tool.image_to_string(
        Image.open(path),
        lang=OCR_LANG,
        builder=pyocr.builders.TextBuilder()
    )
    path = '%s_%s.%s' % (path, timestamp, OCR_FILE_EXTENSION)
    with open(path, 'w') as f:
        f.write(txt)

    print(' ', img, 'OCRed')
    return '%s_%s.%s' % (img, timestamp, OCR_FILE_EXTENSION)
    

def open_read_file_list(base_path, name_list):
    txt_list = []
    for txt in name_list:
        path = os.path.join(base_path, txt)
        with open(path, 'r') as f:
            txt_list.append(f.read())
    return txt_list


def report_in_excel(ex, sheetnames, txt_list):
    pattern_head = r'[^\n ]'
    pattern_tail = r'\n\n \n'

    for sheetname, txt in zip(sheetnames, txt_list):
        available = [name for name in ex.get_sheetnames() if name not in sheetnames]
        if len(available) == 0: # add new sheet if all sheets are already used
            ex.add_sheet(sheetname)
        else: # rename and use available one
            ex.set_sheet_name(available[0], sheetname)

        next_pos = 0 # initial search position in txt
        col_idx  = 2 # initial column to write in
        txt += ' '   # for slicing by -1
        while next_pos < len(txt):
            pos, end = cut_out_txt(txt[next_pos:], pattern_head, pattern_tail)

            data = []
            for line in io.StringIO(txt[next_pos + pos:next_pos + end]):
                idx = line.find(' ')
                if line[:idx].replace('.', '').replace(',', '').isdecimal() \
                    and len(line[:idx]) > 1:
                    data.append([line[:idx], line[idx+1:]])
                else:
                    data.append([line])

            ex.set_range_values(sheetname, 2, col_idx, data)
            col_idx += REPORT_COLUMN_SPAN + 2
            next_pos += end


def cut_out_txt(txt, pattern_head, pattern_tail):
    match = re.search(pattern_head, txt)
    if not match:
        print('Pattern for head not found')
        exit(1)
    idx = match.start()

    match = re.search(pattern_tail, txt[idx:])
    if not match:
        return idx, len(txt)
    return idx, idx + match.end()


async def async_run(iters, cb, *args):
    semaphore = asyncio.Semaphore(ASYNC_PARALLEL_LIMIT)
    async def async_semaphore(cd, *args):
        async with semaphore:
            return await async_executor(cb, *args)

    return await asyncio.gather(
        *[async_semaphore(cb, iter, *args) for iter in iters]
    )


async def async_executor(cb, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, cb, *args)

