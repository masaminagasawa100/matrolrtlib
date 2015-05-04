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

buf = create_string_buffer(str(os.getpid()).encode(),size=5)

read_buf = create_string_buffer(b'',size=5)


@make_aperiod_task(TESTSTRUCT)
def aperiodic_shm_test(i):
    try:
        ret = matrolrt_print("aperiod task a:%d,b:%d\n",i.a,i.b)
        ret = matrolrt_pipe_write(task,byref(buf),size=5)
        matrolrt_pipe_read(task,buf=byref(read_buf),size=5)
        matrolrt_print("read_buf:%s\n",read_buf)
        matrolrt_task_sleep(500000000) #500 ms delay
    except:
        print(traceback.print_exc())



@make_period_task(1000000000,TESTSTRUCT)
def peroidic_shm_test(i):
    ret = matrolrt_print("period task a:%d,b:%d\n",i.a,i.b)
try:

    arg = TESTSTRUCT(1,3)
    task = matrolrttask(b"test2",aperiodic_shm_test,arg)

    task = matrolrt_create_pipe(task,1024,pipe_name="test_pipe",mode=MATROLRT)


    matrolrt_task_spawn(task,cpu_id=0)


    while True:
        time.sleep(10)


except:
    print(traceback.print_exc())
    #matrolrt_pipe_delete(task)
