from PIL import Image, ImageOps, ImageDraw, ImageFont
import base64
from io import BytesIO
import io
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
# memeforge_functions.py

def meme_maker(image, top_text, bottom_text, font_path='impact.ttf', font_size=140):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text length using textlength method
    top_text_length = draw.textlength(top_text, font=font)
    bottom_text_length = draw.textlength(bottom_text, font=font)

    # Calculate text position
    top_text_position = ((image.width - top_text_length) //  2,  10)
    bottom_text_position = ((image.width - bottom_text_length) //  2, image.height - bottom_text_length -  10)

    # Draw text on the image
    draw.text(top_text_position, top_text, font=font, fill="white")
    draw.text(bottom_text_position, bottom_text, font=font, fill="white")

    return image
