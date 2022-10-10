from google.cloud import vision
from google.cloud import vision_v1
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import glob
import pytesseract
import io


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'visionKey.json'


FONT_SIZE = 10
COLOR = 'maroon'


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'


# get source image
def get_image(img):
    img = cv2.imread(r'Samples/{}'.format(img), 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
