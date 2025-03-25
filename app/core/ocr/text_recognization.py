from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, cpu_threads=2) 

def text_recognize(image):
    res = ocr.ocr(image, cls=True)
    if res and res[0] and res[0][0]:
        return res[0][0][1]
    return None
