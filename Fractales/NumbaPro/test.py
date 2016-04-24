from numba import autojit

@autojit
def increment(x):
    return x+1

x = 1
x = increment(x)
