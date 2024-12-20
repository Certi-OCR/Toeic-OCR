from paddleocr import PaddleOCR

def text_recognize(image):
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=True)
    res = ocr.ocr(image, cls=True)
    if res and res[0] and res[0][0]:
        return res[0][0][1]
    return None
    