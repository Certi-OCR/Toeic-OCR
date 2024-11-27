from ultralytics import YOLO
from .image_utils import bytes2image
from .image_processing import processImage
import pandas as pd

def predictions_to_df(results: list, labeles_dict: dict) -> pd.DataFrame:
    predict_bbox = pd.DataFrame(results[0].to("cpu").numpy().boxes.xyxy, columns=['xmin', 'ymin', 'xmax', 'ymax'])
    predict_bbox['confidence'] = results[0].to("cpu").numpy().boxes.conf
    predict_bbox['class'] = (results[0].to("cpu").numpy().boxes.cls).astype(int)
    predict_bbox['name'] = predict_bbox["class"].replace(labeles_dict)
    return predict_bbox

def image_predictions(model: YOLO, file) -> pd.DataFrame:
    input = processImage(bytes2image(file))
    predictions = model.predict(source=input, conf=0.5, imgsz=640, augment=False)  
    df = predictions_to_df(predictions, model.names) 
    return df