#!/bin/env python3

import pickle
import os

def bytes_to_str(data):
    return ' '.join(['%.2X' % (x,) for x in data])

number_of_goods = int(input('Сколько товаров хотят пираты? '))


class Variant:
    def __init__(self):
        self.state = True
        self.blocks = list()
        self.values = set()
        self.blocks_values = list()

    def add(self, data:bytes):
        values = list()
        for i in range(5):
            value = int.from_bytes(data[i*4: (i + 1)*4], byteorder="little")
            if not 0 <= value <= 32: #1 <= value <= number_of_goods:
                self.state = False
                return
            values.append(value)
        self.values = self.values.union(set(values))
        if len(self.values) > number_of_goods:
            self.state = False
            return
        self.blocks.append(data)
        if len(self.blocks) > 1 and len(set(self.blocks)) + 1 < len(self.blocks):
            self.state = False
            return
        self.blocks_values.append(values)


if os.path.exists('./mem.vars'):
    vars = pickle.load(open('./mem.vars', 'rb'))
    first = False
else:
    vars = dict()
    first = True
dump = pickle.load(open('./mem.dump', 'rb'))
    

index = 1
if first:
    print('Запаситесь терпением и отложите игру, не выключая её. Это НА ДОЛГО ;)')
    for key in dump.keys():
        print(f'{index}/{len(dump)} {key}')
        index += 1
        offset = 0
        last_percent = -1
        while offset + 20 < len(dump[key]):
            variant = Variant()
            variant.add(dump[key][offset: offset + 20])
            if variant.state:
                vars[(key, offset)] = variant
            offset += 4
            percent = int(offset * 100.0/len(dump[key]))
            if percent != last_percent:
                print(f'{percent:3d}% ({len(vars)})', end='\r')
                last_percent = percent
        print(f'100% ({len(vars)})')
else:
    new_vars = dict()
    for key, offset in vars.keys():
        if key in dump and offset + 20 < len(dump[key]):
            vars[(key, offset)].add(dump[key][offset: offset + 20])
            if vars[(key, offset)].state:
                new_vars[(key, offset)] = vars[(key, offset)]
        print(f'{index}/{len(vars)} ({len(new_vars)})', end='\r')
        index += 1
    vars = new_vars

print(f'{len(vars)}')
if len(vars) < 10:
    for key, offset in vars.keys():
        variant = vars[(key, offset)]
        print(key)
        print(f'{offset}    ({len(variant.values)})    {variant.values}')
        for block, bvalues in zip(variant.blocks, variant.blocks_values):
            print(f'    {bytes_to_str(block)}    ({len(set(bvalues))})    {bvalues}')
        
print('Сохранение...')
pickle.dump(vars, open('mem.vars', 'wb'))

if len(vars) == 1:
    for _key, _offset in vars.keys():
        key, offset = _key, _offset
    variant = vars[(key, offset)]
    print(f'\n\nОтвет: {variant.blocks_values[-1]}')
    open('./history', 'a').write(f'{key}\t{offset}\n')
