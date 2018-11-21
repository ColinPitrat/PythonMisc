#!/usr/bin/python
# -*- coding: utf8 -*-"

from __future__ import print_function

import sys
import struct

LABELS_FILE_MAGIC = 2049
IMAGES_FILE_MAGIC = 2051

def read_labels(filename):
    with open(filename, 'rb') as f:
        magic = struct.unpack('>i', f.read(4))[0]
        if magic != LABELS_FILE_MAGIC:
            raise RuntimeError("Invalid file type for labels: %s, expected %s" % (magic, LABELS_FILE_MAGIC))
        nb_labels = struct.unpack('>i', f.read(4))[0]
        print("Reading %d labels" % nb_labels)
        result = [struct.unpack('B', f.read(1))[0] for i in range(0, nb_labels)]

    return result

def read_images(filename):
    with open(filename, 'rb') as f:
        magic = struct.unpack('>i', f.read(4))[0]
        if magic != IMAGES_FILE_MAGIC:
            raise RuntimeError("Invalid file type for images: %s, expected %s" % (magic, IMAGES_FILE_MAGIC))
        nb_images = struct.unpack('>i', f.read(4))[0]
        nb_rows = struct.unpack('>i', f.read(4))[0]
        nb_columns = struct.unpack('>i', f.read(4))[0]
        print("Reading %d images" % nb_images)
        result = []
        for i in range(0, nb_images):
            image = []
            for j in range(0, nb_columns):
                image.append([struct.unpack('B', f.read(1))[0] for k in range(0, nb_rows)])
            result.append(image)

    return result

def image_to_string(image):
    for i in range(0, len(image)):
        line = ""
        for j in range(0, len(image[0])):
            if image[i][j] == 0:
                line += " "
            elif image[i][j] < 127:
                line += "."
            else:
                line += "#"
        print(line)

try:
    from PIL import Image
except ImportError:
    print("PIL package not found, generation of image will not be available", file=sys.stderr)
else:
    def image_to_png(image, filename):
        size = (len(image), len(image[0]))
        data = "".join([chr(p) for line in image for p in line])
        img = Image.frombytes('L', size, data)
        #img = Image.frombytes('L', (10, 10), "".join([chr(2*i) for i in range(0, 100)]))
        #img = Image.frombytes('L', (28, 28), "".join([chr(i%256) for i in image[j]]))
        img.save(filename)
