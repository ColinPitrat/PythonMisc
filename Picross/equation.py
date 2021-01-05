#!/usr/bin/python
# -*- coding: utf8 -*-"

import math

a = None
b = None
c = None
d = None
e = None
f = None
g = None
h = None
i = None

# Answer is abcdefghi-a'b'c'd'e'f'g'h'i'
# with a/de + b/fg + c/hi = 1
# and a'/d'*e' + b'/f'*g' + c'/h'*i' = 1
# There are multiple answers possible
# One of them is 579346812 - 157368924 = 421977888
def compute():
  return term1() + term2() + term3()

def _term1():
  return a/(d*10+e)

def _term2():
  return  b/(f*10+g)

def _term3():
  return c/(h*10+i)

def term1():
  return a/(d*e)

def term2():
  return  b/(f*g)

def term3():
  return c/(h*i)

count = 0
for a in range(1, 10):
  for d in range(1, 10):
    if d == a:
        continue
    for e in range(1, 10):
      if e == d or e == a:
        continue
      if term1() > 1:
        continue
      for b in range(1, 10):
        if b == a or b == e or b == d or b < a:
          continue
        for f in range(1, 10):
          if f == a or f == e or f == d or f == b:
            continue
          for g in range(1, 10):
            if g == a or g == e or g== d or g == b or g == f:
              continue
            if term1() + term2() > 1:
              continue
            for c in range(1, 10):
              if c == a or c == e or c== d or c == b or c == f or c == g or c < b:
                continue
              for h in range(1, 10):
                if h == a or h == e or h== d or h == b or h == f or h == g or h == c:
                  continue
                for i in range(1, 10):
                  if i == a or i == e or i== d or i == b or i == f or i == g or i == c or i == h:
                    continue
                  if math.isclose(term1() + term2() + term3(), 1, abs_tol=0.0000001):
                    print("(%d, %d, %d, %d, %d, %d, %d, %d, %d)" % (a, b, c, d, e, f, g, h, i))
                  count += 1
print("%s possibilities" % count)
