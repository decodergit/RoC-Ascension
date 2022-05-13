import gdb
import pickle

wrong_words = {
    'dalvik', 'boot', 'font', 'Chrome', 'kgsl', 'system', 'lib', 'Audio', 
    'System', '.dat', '/dev/__properties__', 'dex', 'apk', 'web', 'config', 
    'cfi', 'binder', '.bss', 'thread', 'bionic'}
mem_obj = dict()

def mem_snapshot(line:str):
    try:
        line = line.split()
        start = line[0]
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
        good = True
        for word in wrong_words:
            if word in objfile:
                good = False
                break
        if not good:
            return None
        offset = 0
        dump = bytes()
        bytes_str = ''
        start_int = int(start, 16)
        print(size, objfile)
        while offset < size:
            dump_str = gdb.execute(f'x/{min(128, size - len(bytes_str)/2)}xb {start_int + offset}', to_string=True)
            for line in dump_str.split('\n'):
                for s in line.split()[1:]:
                    bytes_str += s[2:]
            offset += 128
        dump = bytes.fromhex(bytes_str)
        return (start, size, objfile, dump)
    except:
        return None
    
mem = dict()
for line in gdb.execute('info proc mappings', to_string=True).split('\n')[4:]:
    record = mem_snapshot(line)
    if record:
        print((record[0], record[1], record[2]))
        mem[(record[0], record[1], record[2])] = record[3]
index = int(open('./index', 'r').read())
pickle.dump(mem, open(f'{index:03d}.dump', 'wb')) 
pickle.dump(mem_obj, open('mem_obj.dump', 'wb'))    
