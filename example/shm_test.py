__author__ = 'root'

from lib.native import *
import time
from ctypes import *


class TESTSTRUCT(Structure):
    _fields_ = [
        ('a',c_int),
        ('b',c_int)
    ]





@make_period_task(1000000000,TESTSTRUCT)
def shm_test(i):
    ret = matrolrt_print("a:%d,b:%d\n",i.a,i.b)

    #matrolrt_task_sleep(500000000) # sleep 500us


#shm_test(pointer(c_int(14)))

arg = TESTSTRUCT(1,3)
print(arg.a,arg.b)
task = matrolrttask(b"test",shm_test,pointer(arg))

ret = matrol_task_spawn(task)
while True:
    time.sleep(10)