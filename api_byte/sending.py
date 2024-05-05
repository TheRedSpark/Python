import requests
from PIL import Image
import io

def image_to_byte_array(image_path):
    img = Image.open(image_path)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img.format)
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

image_path = '1.png'

image_bytes = image_to_byte_array(image_path)

url = 'https://media.craft-stock.com:8443/upload'

headers = {'Content-Type': 'image/jpeg'}

response = requests.post(url, data=image_bytes, headers=headers)

print(response.text)
