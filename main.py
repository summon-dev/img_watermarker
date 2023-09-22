from tkinter import *

from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageOps


# Create Class for button with possibility to get the function result
class MyButton(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self.data = None

    def clicked(self, func, *args, **kwargs):
        self.data = func(*args, **kwargs)


def print_out():
    print(open_button.data)


def open_file():
    # Call open file dialog
    file_name = filedialog.askopenfilename()
    # save the image path in a raw string
    file_path = r"{}".format(file_name)
    # print(file_path.rsplit('/', 1)[0])
    print_out()
    return file_path


def watermark_text(file_path, text):
    # Load the image using PIL with RGB format
    image = Image.open(file_path).convert("RGBA")

    # Correcting image orientation
    image = ImageOps.exif_transpose(image)
    position = (image.size[0] - 600, image.size[1] - 300)
    # print(image.size[0])
    # print(image.size[1])

    # Blank image
    img_txt = Image.new("RGBA", image.size, (255, 255, 255, 0))
    # print(img_txt.size[0])
    # print(img_txt.size[1])
    # Get a font
    fnt = ImageFont.truetype("arial.ttf", 150)

    # Create base to draw
    draw = ImageDraw.Draw(image)

    # Draw white Box
    bbox = draw.textbbox(position, text, font=fnt)
    draw.rectangle(bbox, fill="white")

    # draw text on image
    draw.text(position, text=text, font=fnt, fill=(0, 0, 0, 255))

    # compose text image and original image to make it watermarked
    watermarked_img = Image.alpha_composite(image, img_txt)
    # print(watermarked_img.size[0])
    # print(watermarked_img.size[1])
    # watermarked_img.show()
    out_file = file_path.rsplit(
        '/', 1)[0] + '/out/' + file_path.rsplit('/', 1)[1]
    print(out_file)

    watermarked_img = watermarked_img.convert('RGB')
    watermarked_img.save(out_file)

    # watermarked_img.show()

    return watermarked_img

    # return watermarked image


window = Tk("Image WaterMarker")
window.title("Image Watermarker")
window.minsize(width=400, height=100)
window.config(padx=20, pady=20)

my_label = Label(text="Select Source File:", font=("Arial", 10))
my_label.config(padx=5, pady=5)
my_label.grid(column=0, row=0)
open_button = MyButton(
    text="Open File", command=lambda: open_button.clicked(open_file))
open_button.config(padx=5, pady=5)
open_button.grid(column=1, row=0, sticky=W)
label_wtmk = Label(text="Enter Watermark Text:", font=("Arial", 10))
label_wtmk.grid(column=2, row=0, sticky=E)
label_wtmk.config(padx=5, pady=5)
blank_label = Label(text="              ", font=("Arial", 10))
blank_label.grid(column=0, row=1, columnspan=4)
input = Entry()
input.grid(column=3, row=0)

if open_button.data != None:
    print("the open button data -> " + open_button.data)

print_button = MyButton(window, text="Create", command=lambda: print_button.clicked(
    watermark_text, open_button.data, input.get()))
# print(open_button.data)
print_button.grid(column=0, row=2, columnspan=4)
print_button.config(padx=50, pady=5)


window.mainloop()
