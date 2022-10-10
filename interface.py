from fileinput import filename
import tkinter as tk
from tkinter import Canvas, filedialog, Text
import os
from main import main

root = tk.Tk()


def openImage():
    filename = filedialog.askopenfilename(
        initialdir='/', title='Select File', filetype=(("jpeg files", "*.jpg"), ("all files", "*.*")))

    print(filename)


canvas = tk.Canvas(root, height=800, width=700, bg='#263D42')
canvas.pack()

frame = tk.Frame(root, bg='white')
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)


openFile = tk.Button(root, text='Open Image', padx=10,
                     pady=5, fg='white', bg='#263D42', command=openImage)

getPlate = tk.Button(root, text='Get Plate', padx=10,
                     pady=5, fg='white', bg='#263D42', command=main)

openFile.pack(side=tk.LEFT)
getPlate.pack(side=tk.LEFT)


root.mainloop()
