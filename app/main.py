from fastapi import FastAPI, File
from fastapi.responses import StreamingResponse, JSONResponse
from ultralytics import YOLO
from pandas import json_normalize
from .image_utils import bytes2image, image2bytes
from .inference import image_predictions
from .image_processing import processImage
from .text_recognization import text_recognize
from .render_bbox import add_bboxs_on_img


app = FastAPI()
model = YOLO("model/toeicLR.pt")

@app.get("/")
async def root():
 return {"message": "Hello, World!"}

@app.post("/img_to_json")
async def extract_information_from_image(file: bytes = File(...)):
    input_image = bytes2image(file)
    img_trans = processImage(input_image)
    predict = image_predictions(model, file)
    detect_res = predict[['name', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax']]
    texts = []
    
    for index, row in detect_res.iterrows():
        xmin, ymin, xmax, ymax = row[['xmin', 'ymin', 'xmax', 'ymax']].astype(int)
        cropped_image = img_trans[ymin:ymax, xmin:xmax]
        text = text_recognize(cropped_image)
        texts.append({'content': text[0], 'confidence': text[1]})
    
    detect_res['text'] = texts
    return JSONResponse(content=detect_res[['name', 'confidence', 'text']].to_dict(orient='records'))
    

@app.post("/img_to_img")
def image_to_image_with_bounding_boxes(file: bytes = File(...)):
    input_image = bytes2image(file)
    predict = image_predictions(model, file)
    img_with_bbox = add_bboxs_on_img(input_image, predict)
    return StreamingResponse(content=image2bytes(img_with_bbox), media_type="image/png")
