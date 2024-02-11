from PIL import Image, ImageOps
import base64
from io import BytesIO
import IPython.display as display

def imageToBase64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    img_str = img_str.decode('utf-8')
    return img_str

def base64toImage(base64string):
    img_str = base64.b64decode(base64string)
    image = Image.open(BytesIO(img_str))
    return image

