import gdb
import pickle

def mem_pair(line:str):
    try:
        line = line.split()
        start = line[0]
        size = int(line[2], 16)
        return (start, size)
    except:
        return None

mem = set()
for line in gdb.execute('info proc mappings', to_string=True).split('\n')[4:]:
    record = mem_pair(line)
    if record:
        mem.add(record)
pickle.dump(mem, open('first.dump', 'wb'))    
    
