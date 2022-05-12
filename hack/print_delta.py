#!/bin/env python3

import pickle

delta = pickle.load(open('delta.dump', 'rb'))
for x in delta:
    print(x)
    print('-' * 20)
