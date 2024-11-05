from PIL import Image
from inference_sdk import InferenceHTTPClient

def image_predictions(img, api_key):
    CLIENT = InferenceHTTPClient("https://detect.roboflow.com", api_key)
    result = CLIENT.infer(img, "toeic/3")
    predictions =  result.get('predictions', [])
    
    cropped_images = {}
    for pred in predictions:
        x = int(pred['x'])
        y = int(pred['y'])
        width = int(pred['width'])
        height = int(pred['height'])
        class_name = pred['class']
        x -= width // 2
        y -= height // 2
        crop = img[y:y+height, x:x+width]
        cropped_images[class_name] = crop
    return cropped_images
