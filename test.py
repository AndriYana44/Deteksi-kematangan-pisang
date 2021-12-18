# Third party modules
import numpy
from PIL import Image


def get_image(image_path):
    image = Image.open(image_path, "r")
    width, height = image.size
    pixel_values = list(image.getdata())
    channels = 3
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values

def getAverage(item):
    red = 0
    green = 0
    blue = 0
    lenData = 0
    for item1 in item:
        for item2 in item1:
            red += item2[0]
            green += item2[1]
            blue += item2[2]
            lenData += 1
        lenData += 1
    return [round(red/lenData), round(green/lenData), round(blue/lenData)]


path_mentah = 'image/mentah/'
path_matang = 'image/matang/'
path_sangat_matang = 'image/sangat-matang/'

image = get_image(path_mentah + "4.jpeg")
# image = get_image(path_matang + "2.jpeg")
# image = get_image(path_sangat_matang + "5.jpeg")
rgb = getAverage(image)

# cek kematangan berdasarkan warna RGB
if (rgb[0] - rgb[1]) < 17 and (rgb[0] - rgb[1]) > 8:
    print('sangat matang')
elif (rgb[0] - rgb[1]) < 8 and (rgb[0] - rgb[1]) > 0 :
    print('matang')
elif (rgb[0] - rgb[1]) < 0 :
    print('mentah')
else :
    print('tidak terdeteksi')


# print(len(image[0][0]))
# print(image[0][0])
# print(image.shape)
print(rgb)
print(rgb[0] - rgb[1])