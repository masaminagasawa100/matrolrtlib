from MatrolRTlib import *
from ctypes import *
from lib.native_type_def import  *
import time

rt_heap_bind = nativelib.rt_heap_bind
rt_heap_bind.argtypes = [POINTER(RT_HEAP),c_char_p,RTIME]
rt_heap_bind.restype = c_int


rt_heap_unbind = nativelib.rt_heap_unbind
rt_heap_unbind.argtypes = [POINTER(RT_HEAP)]
rt_heap_unbind.restype = c_int


rt_heap_create = nativelib.rt_heap_create
rt_heap_create.argtypes = [POINTER(RT_HEAP),c_char_p,size_t,c_int]
rt_heap_create.restype = c_int

rt_heap_delete = nativelib.rt_heap_delete
rt_heap_delete.argtypes = [POINTER(RT_HEAP)]
rt_heap_delete.restype = c_int


rt_task_create = nativelib.rt_task_create
rt_task_create.argtypes = [c_int]
rt_task_create.restype = c_int

heap_des = RT_HEAP()
print (heap_des)
s = b'some_shm'
c_s = c_char_p(s)
print (c_s)
ret = rt_heap_create(byref(heap_des),c_s,1000,H_SHARED)
print ('rt_heap_create:',ret)
ret = rt_heap_delete(byref(heap_des))
print ('rt_heap_delete:',ret)

while True:
    time.sleep(10)