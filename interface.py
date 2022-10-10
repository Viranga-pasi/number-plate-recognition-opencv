from cProfile import label
from fileinput import filename
import tkinter as tk
from tkinter import *

from tkinter import Canvas, filedialog, Text
import os
from PIL import Image, ImageTk


from main import main

root = tk.Tk()

# open image


def openImage():
    filename = filedialog.askopenfilename(
        initialdir='F:\3rd Yr\CS 314 - Image Processing Practical\Project\Project\Samples', title='Select File', filetype=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))
    main(filename)

    display_original(filename)
    display_output()
    print(filename)


def display_original(filename):
    img = Image.open(filename)
    img.thumbnail((350, 350))
    img = ImageTk.PhotoImage(img)
    original_img.configure(image=img)
    original_img.image = img


def display_output():
    # img = Image.open(filename)
    # img.thumbnail((350, 350))
    img = ImageTk.PhotoImage(Image.open(
        "F://3rd Yr//CS 314 - Image Processing Practical//Project//Project//NumberPlateDetection//crop.jpg"))
    output_img.configure(image=img)
    output_img.image = img


# create canvas
canvas = tk.Canvas(root, height=600, width=400, bg='#263D42')
canvas.pack()

# create middle frame
frame = tk.Frame(root, bg='white')
frame.place(relwidth=0.8, relheight=0.7, relx=0.1, rely=0.1)

# disply first image
original_img = Label(frame)
original_img.pack()

# disply output image
output_img = Label(frame)
output_img.pack()

# buttons
openFile = tk.Button(root, text='Open Image', padx=10,
                     pady=5, fg='white', bg='#263D42', command=openImage)
openFile.pack()

getPlate = tk.Button(root, text='Exit', padx=10,
                     pady=5, fg='white', bg='#263D42', command=lambda: exit())

getPlate.pack()


root.title("Number Plate Reader")
root.mainloop()
