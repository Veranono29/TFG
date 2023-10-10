import pyopencl as cl
from hashlib import md5
platforms = cl.get_platforms()
my_platform = platforms[0] 
print(my_platform.vendor)

devices = my_platform.get_devices()
print(devices)
my_device = devices[0]
print(my_device.name)

ctx = cl.Context([my_device])

cpq = cl.command_queue_properties
queue = cl.CommandQueue(ctx,my_device,cpq.PROFILING_ENABLE)
# end
# bloques, + hilos por bloques; colescencia de memoria; tutoriales de opencl + configuraciones de bloque + numeros de threads por bloque
import numpy
import numpy.linalg as la
#a = numpy.random.rand(5000).astype(numpy.float32)
a = numpy.full(50000,2).astype(numpy.float32)
b = numpy.full(50000,2).astype(numpy.float32)

mf = cl.mem_flags
a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, b.nbytes)


#globali localid blockid
prg = cl.Program(ctx, """
                __kernel void sum(__global const float *a,
                __global const float *b,
                __global float *c)
                 {
                 int gid = get_global_id(0);
                 if (gid>=50000){
                    return;
                 }
                 c[gid] = a[gid] + b[gid];
                 
                 }
""").build()

# tuto + lista palabras md5/md4 -> Transformar a algo entendible
"""
coalescencia de mmeoria -> Todas las plaabras el mismo ancho -> Si hay distnto tm ordenar por tamaño

Copiar con tam max y en GPU recortar hasta /0
Check if Py añade /0

1r0 hash num, 2 hash pala
"""
globalrange = (50000, 1)
#prg.sum(queue, a.shape, None , a_buf,b_buf,dest_buf)
prg.sum(queue, globalrange, None , a_buf,b_buf,dest_buf)

a_plus_b = numpy.empty_like(a)


#Time it
from timeit import default_timer as tm
start = tm()
cl._enqueue_read_buffer(queue,dest_buf, a_plus_b).wait()
#c = a+b
end = tm()


print(end - start)
print(a_plus_b)
#print("Error: ", la.norm(a_plus_b-(a+b)))
