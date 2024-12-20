from PIL import Image
import io

def bytes2image(binary_image: bytes) -> Image:
    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    return input_image

def image2bytes(image: Image) -> bytes:
    return_image = io.BytesIO()
    image.save(return_image, format='JPEG', quality=85)
    return_image.seek(0)
    return return_image