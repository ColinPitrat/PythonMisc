# -*- coding: utf-8 -*-
import timeit
import numpy
import pylab
from numba import autojit

@autojit
def mandel(x, y, max_iters):
    i = 0
    c = complex(x,y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i

    return max_iters

@autojit
def create_fractal(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            color = mandel(real, imag, iters)
            image[y, x] = color

    return image

image = numpy.zeros((500 * 2, 750 * 2), dtype=numpy.uint8)
s = timeit.default_timer()
create_fractal(-2.0, 1.0, -1.0, 1.0, image, 20)
e = timeit.default_timer()
print('time: %f' % (e - s,))
pylab.imshow(image)
pylab.show()
