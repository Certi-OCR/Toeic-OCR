from fastapi import FastAPI, File, Form, status, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image, UnidentifiedImageError
from .image_utils import bytes2image, image2bytes
from .inference import image_predictions
from .image_processing import processImage
from .text_recognization import text_recognize
from .render_bbox import add_bboxs_on_img
import requests

app = FastAPI(
    title="TOEIC OCR API",
    description="API for extracting information from TOEIC uploaded image or URL",
    version="1.0.0",
)
model = YOLO("../model/toeicLR.pt")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def documentation():
    return RedirectResponse("/docs")

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
async def perform_healthcheck():
    return {'Health Check': '200 OK'}

@app.post("/file_to_json")
async def extract_information_from_uploaded_image(file: bytes = File(...)) -> JSONResponse:
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
    return JSONResponse(content=detect_res[['name', 'confidence', 'text']].to_dict(orient='records'))

@app.post("/file_to_bbox")
async def image_to_image_with_bounding_boxes(file: bytes = File(...)) -> StreamingResponse:
    img = bytes2image(file)
    img_trans = processImage(img)
    predict = image_predictions(model, img_trans)
    img_with_bbox = add_bboxs_on_img(img, predict)
    return StreamingResponse(content=image2bytes(img_with_bbox), media_type="image/png")

@app.post("/url_to_json")
async def extract_information_from_url(url: str = Form(...)) -> JSONResponse:
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status() 
        input_image = Image.open(response.raw).convert("RGB")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching image: {e}")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Cannot identify image file")

    bytes_data = image2bytes(input_image)
    bytes_data = bytes_data.getvalue()
    return await extract_information_from_uploaded_image(bytes_data)

@app.post("/url_to_bbox")
async def url_to_image_with_bounding_boxes(url: str = Form(...)) -> StreamingResponse:
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status() 
        input_image = Image.open(response.raw).convert("RGB")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching image: {e}")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Cannot identify image file")

    bytes_data = image2bytes(input_image)
    bytes_data = bytes_data.getvalue()
    return await image_to_image_with_bounding_boxes(bytes_data)