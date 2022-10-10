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


# show images
def show_plot(images, titles):
    # convert all images to gray scale
    plt.style.use('grayscale')

    # to remove background gray
    plt.figure().patch.set_facecolor('white')

    for i in range(len(images)):
        # plt.subplot(len(titles),1,i+1)
        plt.subplot(3, 3, i+1)
        plt.title(titles[i], size=FONT_SIZE, color=COLOR)
        plt.imshow(images[i])
        plt.axis('off')

    plt.show()


# Return binary image by thresholding
def make_binary(img):
    t = 150
    ret, thresh = cv2.threshold(img, t, 255, cv2.THRESH_BINARY_INV)

    return thresh


# Normalize the number plate
def normalize_number_plate(img2):
    img = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    # remove noise
    blur = cv2.bilateralFilter(img, 17, 17, 17)  # 11, 90, 90
    # sharpend_image = cv2.addWeighted(img, 2, blur, -1, 0)

    edges = cv2.Canny(blur, 100, 200)

    cnts, hierarchy = cv2.findContours(
        edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    draw_cnt = cv2.drawContours(img2.copy(), cnts, -1, (255, 0, 0))
    print(len(cnts))

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    draw_cnt_2 = cv2.drawContours(img2.copy(), cnts, -1, (0, 255, 0))
    plt.imshow(draw_cnt, cmap='gray')
    plt.title('Contour')
    plt.show()
    return img, edges, draw_cnt, draw_cnt_2, cnts


# Crop image
def crop_image(cnts, img):
    plate = None
    img3 = img.copy()
    for i in cnts:
        perimeter = cv2.arcLength(i, True)
        edges_count = cv2.approxPolyDP(i, 10, True)

        if len(edges_count) == 4:
            plate = edges_count
            break
    # print(edges_count)
    mask = np.zeros(img.shape, np.uint8)
    new_img = cv2.drawContours(mask, [plate], 0, 255, -1)
    new_img = cv2.bitwise_and(img, img, mask=mask)

    (x, y) = np.where(mask == 255)

    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_img = img[x1-10:x2+10, y1-10:y2+10]
    return new_img, cropped_img
