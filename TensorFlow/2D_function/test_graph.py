#!/usr/bin/python
# -*- coding: utf8 -*-"

from __future__ import absolute_import, division, print_function, unicode_literals

from mpl_toolkits.mplot3d import Axes3D
import math
import matplotlib.pyplot as plt
import numpy as np

def f(x, y):
  return np.sin(x)*np.sin(y)

def main():
  N = 20
  min_x, max_x = 0.0, math.pi
  min_y, max_y = 0.0, math.pi

  dx, dy = max_x - min_x, max_y - min_y
  xs = [[min_x + dx*x/N for x in range(N+1)] for y in range(N+1)]
  ys = [[min_y + dy*y/N for x in range(N+1)] for y in range(N+1)]
  rx = [min_x + dx*x/N for x in range(N+1)]
  ry = [min_y + dy*y/N for y in range(N+1)]
  zs = [[math.sin(x)*math.sin(y) for y in ry] for x in rx]
  zs2 = [[math.sin(x)*y for y in ry] for x in rx]
  print("My z: ", zs)

  # Alternative way to generate the same:
  """
  x = np.linspace(min_x, max_x, N+1)
  y = np.linspace(min_y, max_y, N+1)
  xs, ys = np.meshgrid(x, y)
  zs = f(xs, ys)
  print("NP z: ", zs)
  """

  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.plot_wireframe(xs, ys, np.array(zs), color='r')
  ax.plot_wireframe(xs, ys, np.array(zs2), color='b')
  plt.show()


if __name__ == '__main__':
  main()
