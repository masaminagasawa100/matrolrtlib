__author__ = 'root'

from lib.native import *
import time
from ctypes import *



def shm_test(i):
    c = cast(i,POINTER(c_int)) # must cast the type at first step
    matrolrt_print("%d\n",c.contents.value,init= 1)
    while True:
        ret = matrolrt_print("%d\n",c.contents.value)
        matrolrt_task_sleep(50000000)


#shm_test(pointer(c_int(14)))


task = matrolrttask(b"test",shm_test,pointer(c_int(14)))

ret = matrol_task_spawn(task)
while True:
    time.sleep(10)