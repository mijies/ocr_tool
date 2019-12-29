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
    def __init__(self, data_dir=None):
        self.src_img_list = []
        self.ocr_file_list = []
        if data_dir is None: # make new data directory
            self.data_dir = 'data_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            os.makedirs(self.data_dir)
        else: # use pre-made data directory and source images
            self.data_dir = data_dir
            img_list = glob.glob(os.path.join(data_dir, '*.' + IMG_EXTENSION))
            self.src_img_list = [os.path.split(path)[-1] for path in img_list]


    def print_img_list(self):
        [print(' ', img) for img in self.src_img_list]


    def wget_src_imgs(self, base_url, img_iter):
        if len(self.src_img_list) != 0:
            return

        for img in img_iter:
            res = requests.get(base_url + img)
            if res.status_code != 200:
                return
            if 'image' not in res.headers['content-type']:
                print("Content-Type must be image\n URL: %s\n Content-Type: %s" % (img, content_type))
                exit(1)

            path = os.path.join(self.data_dir, img)
            with open(path, 'wb') as f:
                f.write(res.content)

            self.src_img_list.append(img)


    def ocr_src_imgs(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        for img in self.src_img_list:
            path = os.path.join(self.data_dir, img)
            txt = tool.image_to_string(
                Image.open(path),
                lang=OCR_LANG,
                builder=pyocr.builders.TextBuilder()
            )
            path = '%s%s.%s' % (path, timestamp, OCR_FILE_EXTENSION)
            with open(path, 'w') as f:
                f.write(txt)
            self.ocr_file_list.append(txt)
    

    def report_in_excel(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        report = '%s_%s.%s' % (REPORT_FILE_PREFIX, timestamp, REPORT_FILE_EXTENSION)
        path = os.path.join(self.data_dir, report)
        ex = new_excel_handle(path)

        # pattern_head = r'\n[0-9]'
        pattern_head = r'[^\n ]'
        pattern_tail = r'\n\n \n'
        for img, txt in zip(self.src_img_list, self.ocr_file_list):

            available = [name for name in ex.get_sheetnames() if name not in self.src_img_list]
            if len(available) == 0: # add new sheet if all sheets are already used
                ex.add_sheet(img)
            else: # rename and use available one
                ex.set_sheet_name(available[0], img)

            pos = 0 # initial search position in txt
            col = 2 # initial column to write in
            while pos != -1:
                cut_out, pos = cut_out_txt(txt[pos:], pattern_head, pattern_tail)

                data = []
                for line in io.StringIO(cut_out):
                    idx = line.find(' ')
                    if line[:idx].replace('.', '').replace(',', '').isnumeric():
                        data.append([line[:idx], line[idx+1:]])
                    else:
                        data.append([line])

                ex.set_range_values(img, 2, col, data)
                col += REPORT_COLUMN_SPAN + 2



def cut_out_txt(txt, pattern_head, pattern_tail):
    match = re.search(pattern_head, txt)
    if not match:
        print('Pattern for head not found')
        exit(1)
    idx = match.start()

    match = re.search(pattern_tail, txt[idx:])
    if not match:
        return txt[idx:], -1
    return txt[idx:idx + match.start()], idx + match.end()