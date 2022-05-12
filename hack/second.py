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
    
first_mem = pickle.load(open('first.dump', 'rb'))  

mem = set()
for line in gdb.execute('info proc mappings', to_string=True).split('\n')[4:]:
    record = mem_pair(line)
    if record:
        mem.add(record)
        
delta = list()
for record in mem:
    if record not in first_mem:
        delta.append(record)
        #print(record)
        #s = gdb.execute(f'x/{record[1]}xb {record[0]}', to_string=True)
        #print(s)
pickle.dump(delta, open('delta.dump', 'wb'))    
