import gdb
import pickle

gdb.execute('set pagination off')

def mem_snapshot(line:str):
    try:
        line = line.split()
        start = line[0]
        end = line[1]
        size = int(line[2], 16)
        if len(line) >= 5:
            objfile = line[4]
        else:
            objfile = ''
            return None
        if objfile in mem_obj:
            mem_obj[objfile] = [mem_obj[objfile][0] + 1, mem_obj[objfile][1] + size]
        else:
            mem_obj[objfile] = [1, size]
        if objfile != '[anon:libc_malloc]':
            return None
        offset = 0
        gdb.execute(f'dump binary memory dump.bin {start} {end}')
        dump = open('./dump.bin', 'rb').read()
        return (start, size, objfile, dump)
    except:
        return None
    
mem = dict()
for line in gdb.execute('info proc mappings', to_string=True).split('\n')[4:]:
    record = mem_snapshot(line)
    if record:
        print((record[0], record[1], record[2]))
        mem[(record[0], record[1], record[2])] = record[3]
pickle.dump(mem, open('mem.dump', 'wb')) 
