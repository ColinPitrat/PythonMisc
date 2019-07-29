#!/usr/bin/python
# -*- coding: utf8 -*-"

from __future__ import print_function

import sys
import struct

LABELS_FILE_MAGIC = 2049
IMAGES_FILE_MAGIC = 2051

class Img(object):

    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    def __str__(self):
        result = ""
        for i in range(0, self.height):
            line = ""
            for j in range(0, self.width):
                if self.pixels[i*self.width+j] < 0.01:
                    line += " "
                elif self.pixels[i*self.width+j] < 0.5:
                    line += "."
                else:
                    line += "#"
            result += line + "\n"
        return result


def read_labels(filename, limit=None):
    with open(filename, 'rb') as f:
        magic = struct.unpack('>i', f.read(4))[0]
        if magic != LABELS_FILE_MAGIC:
            raise RuntimeError("Invalid file type for labels: %s, expected %s" % (magic, LABELS_FILE_MAGIC))
        nb_labels = struct.unpack('>i', f.read(4))[0]
        if limit:
            nb_labels = min(limit, nb_labels)
        print("Reading %d labels" % nb_labels)
        result = [struct.unpack('B', f.read(1))[0] for i in range(0, nb_labels)]

    return result

def read_images(filename, limit=None):
    with open(filename, 'rb') as f:
        magic = struct.unpack('>i', f.read(4))[0]
        if magic != IMAGES_FILE_MAGIC:
            raise RuntimeError("Invalid file type for images: %s, expected %s" % (magic, IMAGES_FILE_MAGIC))
        nb_images = struct.unpack('>i', f.read(4))[0]
        if limit:
            nb_images = min(limit, nb_images)
        nb_rows = struct.unpack('>i', f.read(4))[0]
        nb_columns = struct.unpack('>i', f.read(4))[0]
        print("Reading %d images" % nb_images)
        result = []
        for i in range(0, nb_images):
            pixels = [struct.unpack('B', f.read(1))[0]/255.0 for k in range(0, nb_rows*nb_columns)]
            result.append(Img(nb_rows, nb_columns, pixels))

    return result

def image_to_string(image):
    return image.__str__()

try:
    from PIL import Image
except ImportError:
    print("PIL package not found, generation of image will not be available", file=sys.stderr)
else:
    def image_to_png(image, filename):
        size = (image.height, image.width)
        data = "".join([chr(int(p*255)) for p in image.pixels])
        img = Image.frombytes('L', size, data)
        img.save(filename)
