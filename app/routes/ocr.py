from PIL import Image, UnidentifiedImageError
from fastapi import APIRouter, File, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import requests

from app.common.error import BadRequest
from app.core.ocr.model import model
from app.core.ocr.image_processing import processImage
from app.core.ocr.image_utils import bytes2image, image2bytes
from app.core.ocr.inference import image_predictions
from app.core.ocr.render_bbox import add_bboxs_on_img
from app.core.ocr.text_recognization import text_recognize

router = APIRouter()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


@router.post("/file_to_json")
async def extract_information_from_uploaded_image(
    file: bytes = File(...),
) -> JSONResponse:
    input_image = bytes2image(file)
    img_trans = processImage(input_image)
    predict = image_predictions(model, img_trans)
    detect_res = predict[["name", "confidence", "xmin", "ymin", "xmax", "ymax"]]
    texts = []

    for index, row in detect_res.iterrows():
        xmin, ymin, xmax, ymax = row[["xmin", "ymin", "xmax", "ymax"]].astype(int)
        cropped_image = img_trans[ymin:ymax, xmin:xmax]
        text = text_recognize(cropped_image)
        if text is not None:
            texts.append({"content": text[0], "confidence": text[1]})
        else:
            texts.append({"content": None, "confidence": None})

    detect_res["text"] = texts
    return JSONResponse(
        content=detect_res[["name", "confidence", "text"]].to_dict(orient="records")
    )


@router.post("/file_to_bbox")
async def image_to_image_with_bounding_boxes(
    file: bytes = File(...),
) -> StreamingResponse:
    img = bytes2image(file)
    img_trans = processImage(img)
    predict = image_predictions(model, img_trans)
    img_with_bbox = add_bboxs_on_img(img, predict)
    return StreamingResponse(content=image2bytes(img_with_bbox), media_type="image/png")


@router.post("/url_to_json")
async def extract_information_from_url(url: str = Form(...)) -> JSONResponse:
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        input_image = Image.open(response.raw).convert("RGB")
    except requests.exceptions.RequestException as e:
        raise BadRequest(message=f"Error fetching image: {e}")
    except UnidentifiedImageError:
        raise BadRequest(message="Cannot identify image file")

    bytes_data = image2bytes(input_image)
    bytes_data = bytes_data.getvalue()
    return await extract_information_from_uploaded_image(bytes_data)


@router.post("/url_to_bbox")
async def url_to_image_with_bounding_boxes(url: str = Form(...)) -> StreamingResponse:
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        input_image = Image.open(response.raw).convert("RGB")
    except requests.exceptions.RequestException as e:
        raise BadRequest(message=f"Error fetching image: {e}")
    except UnidentifiedImageError:
        raise BadRequest(message="Cannot identify image file")

    bytes_data = image2bytes(input_image)
    bytes_data = bytes_data.getvalue()
    return await image_to_image_with_bounding_boxes(bytes_data)
