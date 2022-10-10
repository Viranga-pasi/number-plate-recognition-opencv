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


# return province on call
def get_province(text):

    provinces = {'SP': 'Southern Province',
                 'WP': 'Western Province',
                 'EP': 'Eastern Province',
                 'NP': 'Nothern Province',
                 'NW': 'North Western Province',
                 'SG': 'Sabaragamuwa Province',
                 'CP': 'Central Province',
                 'NC': 'North Central Province',
                 'UW': 'Uwa Province',
                 }

    if text in provinces.keys():
        return provinces[text]

    else:
        return 'Province cannot detected'


# return vehicle type on call
def get_vehicle_type(text):
    v_type = None

    # if text is a string
    if text.isalpha():
        print(text)
        to_array = list(text)
        # cars
        print(to_array)
        if to_array[0] == 'C' or to_array[0] == 'K':
            v_type = 'Car'
        # Bike
        elif to_array[0] == 'M' or to_array[0] == 'T' or to_array[0] == 'U' or to_array[0] == 'V' or to_array[0] == 'W' or to_array[0] == 'X' or to_array[0] == 'B':
            v_type = 'Bike'
        # Bus
        elif to_array[0] == 'N':
            v_type = 'Bus'
        # Lorry
        elif to_array[0] == 'L' or to_array[0] == 'D':
            v_type = 'Lorry'
        # Threewheel
        elif to_array[0] == 'Q' or to_array[0] == 'Y' or to_array[0] == 'A':
            v_type = 'Threewheel'
        # Dual purpose vehicle
        elif to_array[0] == 'P':
            v_type = 'Dual Purpose Vehicle'
        # Tractor
        elif to_array[0] == 'R':
            v_type = 'Tractor'
        # Land master
        elif to_array[0] == 'S':
            v_type = 'Land master'
        else:
            v_type = 'Vehicle class cannot be detected'

    return v_type
