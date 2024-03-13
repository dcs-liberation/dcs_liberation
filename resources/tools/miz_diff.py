import sys

from dcs.lua.parse import *
from dcs.lua.serialize import *

a = loads(open(sys.argv[1], "r").read())
b = loads(open(sys.argv[2], "r").read())


def get(a, k):
    b = a
    for x in k.strip().split(" "):
        if isinstance(a, dict):
            y = a
            a = a.get(x, None)
            if a is None:
                try:
                    a = y.get(int(x), None)
                except:
                    pass
        else:
            break
    if a is None:
        pass
    return a


def cycle(kk, ref, v):
    if isinstance(v, dict):
        for k, v in v.items():
            cycle(kk + " " + str(k), ref, v)
    elif isinstance(v, list):
        for i, v in enumerate(v):
            cycle(kk + " " + str(i), ref, v)
    else:
        if get(ref, kk) != v:
            print(kk)
            print(v)
            print(get(ref, kk))


cycle("", a, b)
