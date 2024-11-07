from paddleocr import PaddleOCR
import numpy as np
import re

def text_ocr(image):
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=True)
    res = ocr.ocr(image, cls=True)
    # text = ""
    # for r in res:
    #     scores = r[0][1]
    #     if np.isnan(scores):
    #         scores = 0
    #     else:
    #         scores = int(scores * 100)
    #     if scores > 60:
    #         text = r[0][0]
    # pattern = re.compile('[\W]')
    # text = pattern.sub('', text)
    # text = text.replace("???", "")
    # text = text.replace("O", "0")
    # text = text.replace("粤", "")
    # return str(text)
    return res[0][0][1]
    