from PIL import Image

def make_png(file):
    img = Image.open(file)
    img = img.convert("RGBA")

    pixels = img.getdata()
    buffer = []

    for pixel in pixels:
        if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
            buffer.append((255, 255, 255, 0))
        else:
            buffer.append(pixel)

    img.putdata(buffer)
    img.save("transparent_mask.png", "PNG")