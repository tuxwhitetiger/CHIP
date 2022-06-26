#!/usr/bin/python

from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.gpio_slowdown = 3
options.hardware_mapping = 'regular'

matrix = RGBMatrix(options = options)

image = Image.open("./faces/test.gif")
while True:
    matrix.SetImage(image.convert('RGB'))





