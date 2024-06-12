from hashlib import md5
HASH_OBJETIVO = md5("INER-".encode()).hexdigest() # INER- line 11.084.266
filename= "realhuman_phill.txt"
#filename= "rockyou.txt"
f_res_name= "Client\\TestingSubsistema\\zunder_Final_TFG\\multiprocess_stats.csv"
#number_lines = 63941070
#number_lines = 14344391
def convert_size(size_bytes):
        import math
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])