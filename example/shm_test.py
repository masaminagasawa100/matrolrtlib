__author__ = 'root'

from lib.native import *
import time
from ctypes import *


class TESTSTRUCT(Structure):
    _fields_ = [
        ('a',c_int),
        ('b',c_int)
    ]


@make_aperiod_task(TESTSTRUCT)
def aperiodic_shm_test(i):
    ret = matrolrt_print("aperiod task a:%d,b:%d\n",i.a,i.b)
    matrolrt_task_sleep(500000000) #500 ms delay


@make_period_task(1000000000,TESTSTRUCT)
def peroidic_shm_test(i):
    ret = matrolrt_print("period task a:%d,b:%d\n",i.a,i.b)


#shm_test(pointer(c_int(14)))


try:
    arg = TESTSTRUCT(1,3)
    task = matrolrttask(b"test1",peroidic_shm_test,arg)

    matrolrt_create_shm(task,1024)

    while True:
        print("test")
        time.sleep(1)

except Exception as e:
    print(e)
    matrolrt_task_delete(task)
except KeyboardInterrupt:
    matrolrt_task_delete(task)