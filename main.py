from cmath import isnan
from google.cloud import vision
from google.cloud import vision_v1
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import pytesseract
import io


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'visionKey.json'


FONT_SIZE = 10
COLOR = 'maroon'


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'


# get source image
def get_image(img):
    img = cv2.imread(img, 1)
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
        plt.subplot(2, 3, i+1)
        plt.title(titles[i], size=FONT_SIZE, color=COLOR)
        plt.imshow(images[i])
        plt.axis('off')

    plt.show()


# Return binary image by thresholding
def make_binary(img):
    t = 150
    ret, thresh = cv2.threshold(img, t, 255, cv2.THRESH_BINARY_INV)

    return thresh


def bilateral_filter(img):
    blur = cv2.bilateralFilter(img, 17, 17, 17)
    return blur


# Normalize the number plate
def normalize_number_plate(img2):
    img = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    # remove noise
    # blur = cv2.bilateralFilter(img, 17, 17, 17)  # 11, 90, 90

    # sharpend_image = cv2.addWeighted(img, 2, blur, -1, 0)
    blur = bilateral_filter(img)
    edges = cv2.Canny(blur, 100, 200)

    cnts, hierarchy = cv2.findContours(
        edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    draw_cnt = cv2.drawContours(img2.copy(), cnts, -1, (255, 0, 0))
    print(len(cnts))

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    draw_cnt_2 = cv2.drawContours(img2.copy(), cnts, -1, (0, 255, 0))
    # plt.imshow(draw_cnt, cmap='gray')
    # plt.title('Contour')
    # plt.show()
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
def main(filename):
    # get vision
    vision_client = vision.ImageAnnotatorClient()
    image = vision.Image()

    # import image

    #mg2 = get_image('pre.jpg')
    print('location : ', filename)

    img2 = get_image(filename)

    img = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

    blur, edges, draw_cnt, draw_cnt_2, cnts = normalize_number_plate(img2)

    # extract number plate
    plate, crop = crop_image(cnts, img)

    crop = bilateral_filter(crop)
    cv2.imwrite('crop.jpg', crop)
    h, w = crop.shape[::]
    #crop_img = cv2.imread(r'crop.jpg', 0)

    with io.open('crop.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    response = vision_client.text_detection(image=image)
    response = response.text_annotations
    text = response[0].description

    # text = 'wp CAL 2234'

    print(crop.shape)
    print(crop.dtype)
    print(crop)

    # text = 'WP BBF 1233'
    # print(response)

    images = [img2, blur, edges, draw_cnt_2, plate, crop]
    titles = ['original', 'smooth', 'edges',
              'draw_cnt', 'mask image', 'cropped image']

    # show images
    show_plot(images, titles)

    return text


def extract_text(text):

    text = text.replace(' ', '')
    text = text.replace('-', '')
    text = text.replace('+', '')

    number_plate = None
    model = None
    print(text)
    if text[0].isdigit():
        if len(text) == 8:
            model = text[:3]
            number_plate = text[:3] + ' SRI ' + text[4:]
        if len(text) == 7:
            model = text[:2]
            number_plate = text[:2] + ' SRI ' + text[3:]
        if len(text) == 6:
            model = text[:1]
            number_plate = text[:1] + ' SRI ' + text[2:]
    else:
        number_plate = text

    print(number_plate, model)


# extract_text('යුහ 084657')


# 10084654
