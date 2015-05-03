from MatrolRTlib import *
from ctypes import *
from lib.native_type_def import  *

matrolrttaskentrytype = CFUNCTYPE(None,c_void_p)

class matrolrttask():
    def __init__(self,name,func,args):
        if type(name) is str:
            self.name = name.encode()
        else:
            self.name = name
        self.entry = matrolrttaskentrytype(func)
        self.args = args


def matrolrt_print(fmt,*args,task_name=b'task 1',bufsize=4096,init=0):
    if type(fmt) is not bytes:
        fmt = fmt.encode()
    for arg in args:
        if type(arg) is str:
            print(arg +" is the str type,must be convert to '''bytes''' type")
    return matrolrtlib.matrolrt_printf(task_name,bufsize,init,fmt,*args)


def matrol_task_spawn(task,stk_size="16384",pro=1,cpu_id=0):
    if type(task) is not matrolrttask:
        print("task must the type matrolrttask")
        return
    return matrolrtlib.matrolrt_task_spawn(task.name,stk_size,pro,cpu_id,task.entry,task.args)


def matrolrt_task_sleep(time):
    delay = c_ulonglong(time)
    return matrolrtlib.matrolrt_task_sleep(delay)


def matrolrt_task_set_periodic(time):
    period = c_ulonglong(time)
    return matrolrtlib.matrolrt_task_set_peroidic(period)


def matrolrt_task_wait_period():
    overrun_r = c_ulong()
    ret = matrolrtlib.matrolrt_task_wait_period(byref(overrun_r))
    return (ret,overrun_r)



def make_period_task(time, type):
    def _make_period_task(func):
        def __make_period_task(ptr):
            c = cast(ptr,POINTER(type)) # must cast the type at first step
            matrolrt_print("%d\n",c.contents.a,init= 1)
            matrolrt_task_set_periodic(time)
            while True:
                func(c)
                (ret,overrun) = matrolrt_task_wait_period()
                if ret < 0:
                    matrolrt_print("task overrun :%ld\n",overrun)
        return __make_period_task
    return _make_period_task
