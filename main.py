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


from getVehicleDetails import *


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'visionKey.json'


FONT_SIZE = 10
COLOR = 'maroon'


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'


# get source image
def get_image(img):
    img = cv2.imread(r'Samples/{}'.format(img), 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

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


# main funtion
def main():
    # get vision
    vision_client = vision.ImageAnnotatorClient()
    image = vision.Image()

    # import image

    img2 = get_image('pre.jpg')

    img = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

    blur, edges, draw_cnt, draw_cnt_2, cnts = normalize_number_plate(img2)

    # extract number plate
    plate, crop = crop_image(cnts, img)
    cv2.imwrite('crop.jpg', crop)
    h, w = crop.shape[::]
    #crop_img = cv2.imread(r'crop.jpg', 0)

    with io.open('crop.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)

    # response = vision_client.text_detection(image=image)
    # response = response.text_annotations
    # text = response[0].description

    print(crop.shape)
    print(crop.dtype)
    print(crop)

    text = ''
    # print(response)
    print(text)
    print('Number Plate :', text)

    if not text:
        print('Number plate cannot detected')
    else:
        splited_text = text.split()
        print(splited_text)

        # return province
        if splited_text[0].isalpha():
            province = get_province(splited_text[0])
            print(
                'Vehicle Registered in : {} - {} '.format(splited_text[0], province))
        else:
            print('Province Cannot detected')

        # return vehicle type
        type = get_vehicle_type(splited_text[1])
        print('Vehicle class is : {} - {} '.format(splited_text[1], type))

    # images array
    #images = [img2, blur, edges, draw_cnt, draw_cnt_2]
    images = [img2, blur, edges, draw_cnt_2, plate, crop]
    titles = ['original', 'smooth', 'edges',
              'draw_cnt', 'mask image', 'cropped image']

    # show images
    show_plot(images, titles)
