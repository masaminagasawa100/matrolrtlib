__author__ = 'root'

from lib.native import *
import time
from ctypes import *
import  traceback
import os

class TESTSTRUCT(Structure):
    _fields_ = [
        ('a',c_int),
        ('b',c_int)
    ]

read_buf = create_string_buffer(b'',size=5)



@make_aperiod_task(TESTSTRUCT)
def aperiodic_shm_test(i):
    ret = matrolrt_print("period task a:%d,b:%d\n",i.a,i.b)
    ret = matrolrt_queue_read(task,byref(read_buf),size=5)
    if ret >0:
        matrolrt_print("%s",read_buf)
    else:
        matrolrt_print("ret:%d\n",ret)


@make_period_task(1000000000,TESTSTRUCT)
def peroidic_shm_test(i):
    ret = matrolrt_print("period task a:%d,b:%d\n",i.a,i.b)
    ret = matrolrt_pipe_read(task,byref(read_buf),size=5)
    matrolrt_print("ret is:%d\n",ret)



try:

    arg = TESTSTRUCT(1,3)

    task = matrolrttask(b"test1",aperiodic_shm_test,arg)

    task = matrolrt_create_queue(task,1024,queue_name="test_queue")

    matrolrt_task_spawn(task,cpu_id=0)

    while True:
        time.sleep(10)


except:
    print(traceback.print_exc())
    #matrolrt_pipe_delete(task)
