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
    task2 = matrolrttask(b"test2",aperiodic_shm_test,arg)

    task = matrolrt_task_spawn(task,cpu_id=0)
    task2 = matrolrt_task_spawn(task2,cpu_id=1)
    while True:
        time.sleep(10)
except Exception as e:
    print("test")
    print("task1 delete return :%d\n"%matrolrt_task_delete(task))
    print("task2 delete return :%d\n"%matrolrt_task_delete(task2))
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    print("task1 delete return :%d\n"%matrolrt_task_delete(task))
    print("task2 delete return :%d\n"%matrolrt_task_delete(task2))