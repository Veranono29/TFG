import subprocess
from os import cpu_count
for a in range(cpu_count()): subprocess.Popen("python testerClient.py")
