import multiprocessing ,numpy as np ,time, os
from hashlib import md5
from multiprocessing import cpu_count
from ctypes import c_char,c_bool

# HASH_OBJETIVO = md5("INER-".encode()).hexdigest() # INER- line 11.084.266
# filename= "rockyou_limpio.txt"

from OBJETIVOS import *

res = ""


LINE =[
    0
   ,14344392] 
Line_Bytes_Number =[
    0
   ,os.path.getsize(filename=filename)+30] 
def worker(hashes:list[str], result,hay_resultado,HASH_OBJETIVO:str):
    """A worker function to calculate squares of hashes."""
    for i in hashes:
        # print(type(i.value))
        # print(str(i.value))
        # break
        #if hay_resultado.value == True:
        #    break
        md5(i).hexdigest()
        # if md5(i).hexdigest() == HASH_OBJETIVO:
        #     print("REsultado encontrado:", i)
        #     result.value = i
        #     hay_resultado.value= True
        #     break

# opcion f
def bytes_np_fromfile():
    return np.fromfile( filename,dtype=np.byte
                        ,offset=Line_Bytes_Number[0]
                        ,count=Line_Bytes_Number[1]
                    ).tobytes().splitlines()


def main(number_cores:int):
    global res

    start_file_lecture = time.perf_counter()
    hashes = bytes_np_fromfile()
    end_file_lecture = time.perf_counter()
    
    hay_resultado = multiprocessing.Value(c_bool,False)
    result =multiprocessing.Array(c_char,size_or_initializer=70)

    segment = len(hashes) // number_cores
    processes = []

    for i in range(number_cores):
        start = i * segment
        if i == number_cores - 1:
            end = len(hashes)  # Ensure the last segment goes up to the end
        else:
            end = start + segment
        chunk = hashes[start:end]
        # Creating a process for each segment
        p = multiprocessing.Process(target=worker, args=(chunk, result,hay_resultado,HASH_OBJETIVO))
        processes.append(p)
        p.start()
    print("File READ TIME = ",end_file_lecture-start_file_lecture,"LEN_CHUNK = ",segment)
    
    time_start_join = time.perf_counter()
    print("Elapsed time in multiprocess Configuration and initialization = ",time_start_join-end_file_lecture,"Total time: ",time_start_join-start_file_lecture)

    for p in processes:
        p.join()
    
    time_end_main = time.perf_counter()
    print("Time waiting for multiprocess end = ",time_end_main-time_start_join,"Total time: ",time_end_main-start_file_lecture)
    res+=f"{end_file_lecture-start_file_lecture},{segment},{time_start_join-end_file_lecture},{time_end_main-time_start_join},"
    print(result.value.decode())
    return result

if __name__ == '__main__':
    n_cores = 2#cpu_count() # pon el numero de cores que quieras probar
    for a in range(4):#range(8*5-1,8*5): sise descomenta esta linea y la de abajo tienes una comparacion de lo que tarda con distinto numero de procesos(aka cores)
        res=""
        #n_cores=(a//5)+1
        
        with open(f_res_name,"a") as f_csv:
            res += str(n_cores)+","
            print(f"Using {n_cores} cores:")

            start_calculations = time.perf_counter()
            result = main(n_cores)
            end_calculations = time.perf_counter()
            
            res+=f"{end_calculations-start_calculations},\"{os.path.basename(filename)}\"\n"
            f_csv.write(res)
            print(f"Resultado: {result.value}\nTotal Program Time = {end_calculations-start_calculations}")
