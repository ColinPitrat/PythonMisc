#!/usr/bin/python
# -*- coding: utf8 -*-"
from bs4 import BeautifulSoup

import collections
import cv2
from enum import Enum
import os
import random
import shutil

class Behavior(Enum):
    JUST_LINK = 1  # Symbolic link to the original file
    COPY = 2       # Copy the original file
    CROP = 3       # Extract the part of the image containing the dog

behavior = Behavior.CROP

BndBox = collections.namedtuple("BndBox", "xmin xmax ymin ymax")

def ExtractBndBox(d, f):
    fname = 'annotations/Annotation/%s/%s' % (d, f.replace('.jpg', ''))
    with open(fname, 'r') as file:
        bs_content = BeautifulSoup(file.read(), 'html.parser')
        bndbox = bs_content.find_all('bndbox')[0]
        xm = int(bndbox.find('xmin').text)
        xM = int(bndbox.find('xmax').text)
        ym = int(bndbox.find('ymin').text)
        yM = int(bndbox.find('ymax').text)
        return BndBox(xm, xM, ym, yM)

test_pct=10
val_pct=5

if os.path.exists('data'):
    shutil.rmtree('data')

subdirs = ['test', 'train', 'val']

os.mkdir('data')
for s in subdirs:
    os.mkdir('data/%s' % s)
for d in os.listdir('images/Images/'):
    for s in subdirs:
        os.mkdir('data/%s/%s' % (s, d))
    for f in os.listdir('images/Images/%s' % d):
        src = 'images/Images/%s/%s' % (d, f)
        subdir = 'train'
        r = 100*random.random()
        if r < val_pct:
            subdir = 'val'
        elif r < val_pct + test_pct:
            subdir = 'test'
        dst = 'data/%s/%s/%s' % (subdir, d, f)
        if behavior == Behavior.JUST_LINK:
            os.link(src, dst)
        elif behavior == Behavior.COPY:
            shutil.copy(src, dst)
        elif behavior == Behavior.CROP:
            bndbox = ExtractBndBox(d, f)
            img = cv2.imread(src)
            crop_img = img[bndbox.ymin:bndbox.ymax, bndbox.xmin:bndbox.xmax]
            cv2.imwrite(dst, crop_img)
        else:
            raise "Unsupported behavior %s" % behavior
