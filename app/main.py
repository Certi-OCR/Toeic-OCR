from fastapi import FastAPI, File
from ultralytics import YOLO
from .image_utils import bytes2image
from .inference import image_predictions
from .image_processing import processImage
from .text_recognization import text_recognize
import json

app = FastAPI()
model = YOLO("model/toeicLR.pt")

@app.get("/")
async def root():
 return {"message": "Hello, World!"}

@app.post("/detect/")
async def extract_information_from_image(file: bytes = File(...)):
    result = {}
    input_image = bytes2image(file)
    img_trans = processImage(input_image)
    predict = image_predictions(model, img_trans)
    detect_res = predict[['name', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax']]
        
    texts = []
    
    for index, row in detect_res.iterrows():
        xmin, ymin, xmax, ymax = row[['xmin', 'ymin', 'xmax', 'ymax']].astype(int)
        cropped_image = img_trans[ymin:ymax, xmin:xmax]
        text = text_recognize(cropped_image)
        texts.append({'content': text[0], 'confidence': text[1]})
    
    detect_res['text'] = texts
    
    result['results'] = json.loads(detect_res[['name', 'confidence', 'text']].to_json(orient='records'))
    return result