from hashlib import md5
import numpy as np
import time, os
#from os import cpu_count
from OBJETIVOS import *
# filename= "rockyou.txt"
# HASH_OBJETIVO = "d6c4cc859ac86b42115d6f85257012b4"#md5("0 0 0".encode()).hexdigest() 
Line_Bytes_Number =[
    0
   ,os.path.getsize(filename=filename)+30] 
#from itertools import islice


# opcion f
def bytes_np_fromfile():
    return np.fromfile( filename,dtype=np.byte
                        ,offset=Line_Bytes_Number[0]
                        ,count=Line_Bytes_Number[1]
                    ).tobytes().splitlines()

if __name__ == "__main__":
    start = time.perf_counter_ns()
    pstart = time.process_time_ns()

    generator = bytes_np_fromfile()#test_binRead_list()

    ppost_generator = time.process_time_ns()
    post_generator = time.perf_counter_ns()
    for a in generator:
        md5(a).hexdigest()
        if md5(a).hexdigest() == HASH_OBJETIVO:
            print(a," = ", HASH_OBJETIVO)
            break
    end = time.perf_counter_ns()  
    pend = time.process_time_ns()
#HASH_OBJETIVO
#filenameimport math

    def convert_size(size_bytes):
        import math
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
    with open(f_res_name,"a") as f_csv:
        f_csv.write(f"1,{(post_generator-start)/1e9},{len(generator)},0,{(end-post_generator)/1e9},{(end-start)/1e9},\"{filename}\"\n")
    print(f"Wordlist name = {filename}\n WordlistSize = {convert_size(os.path.getsize(filename=filename))}  -  Number of lines = {len(generator)}")
    print(f"Process Read File = {(ppost_generator-pstart)/1e9}  -  Process Hashing md5 Time = {(pend-ppost_generator)/1e9} \n Process Total Process Time = {(pend-pstart)/1e9}")
    print(f"Real Read Time = {(post_generator-start)/1e9}  -  Real Hashing md5 Time = {(end-post_generator)/1e9}  \n  Real Total time = {(end-start)/1e9}")
   