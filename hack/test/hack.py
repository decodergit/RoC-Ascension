#!/bin/env python3

import difflib

file1 = open('./1/roc_1.hprof', 'rb')
file2 = open('./1/roc_2.hprof', 'rb')

#diff = difflib.ndiff(file1.readlines(), file2.readlines())
#delta = ''.join(x[2:] for x in diff if x.startswith('- '))
#print(delta)

for line in difflib.context_diff(file1.read(), file2.read()):
    print(line)
