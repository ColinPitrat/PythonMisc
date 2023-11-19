#!/usr/bin/python
# -*- coding: utf8 -*-"
import os
import random
import shutil

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
        os.link(src, dst)
