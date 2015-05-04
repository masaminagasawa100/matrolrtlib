from MatrolRTlib import *
from ctypes import *
from lib.native_type_def import  *
import errno
import os

libc = CDLL('/lib/x86_64-linux-gnu/libc.so.6')


#######  matrolrt task part #########

def matrolrt_print(fmt,*args,task_name=b'task',bufsize=4096,init=0):
    if type(fmt) is not bytes:
        fmt = fmt.encode()
    for arg in args:
        if type(arg) is str:
            print(arg +" is the str type,must be convert to '''bytes''' type")
    return matrolrtlib.matrolrt_printf(task_name,bufsize,init,fmt,*args)


def matrolrt_task_spawn(task,stk_size="16384",pro=1,cpu_id=0):
    if type(task) is not matrolrttask:
        print("task must the type matrolrttask")
        return
    task.taskinfo.ptr = matrolrtlib.matrolrt_task_spawn(task.taskinfo.name,stk_size,pro,cpu_id,task.taskinfo.entry,task.taskinfo.args)
    return task

def matrolrt_task_delete(task):
    return matrolrtlib.matrolrt_task_delete(task.taskinfo.ptr)


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



def make_period_task(time, argtype):
    def _make_period_task(func):
        def __make_period_task(ptr):
            c = cast(ptr,POINTER(argtype)) # must cast the type at first step
            matrolrt_print("task peroidic start:%s\n",func.__name__.encode(),init=1)
            matrolrt_task_set_periodic(time)
            while True:
                func(c.contents)
                (ret,overrun) = matrolrt_task_wait_period()
                if ret < 0:
                    matrolrt_print("task overrun :%ld\n",overrun)
        return __make_period_task
    return _make_period_task

def make_aperiod_task(argtype):
    def _make_aperiod_task(func):
        def __make_aperiod_task(ptr):
            c = cast(ptr,POINTER(argtype)) # must cast the type at first step
            matrolrt_print("task aperoidic start:%s\n",func.__name__.encode(),init=1)
            while True:
                func(c.contents)
        return __make_aperiod_task
    return _make_aperiod_task



#######  matrolrt shared memory part #########

def matrolrt_create_shm(task,size,shm_name=None):
    shm_desc_ptr = None
    shm_ptr = None
    shared_mem_name = None
    if shm_name is not None: #override the shared memory name
        shared_mem_name = shm_name
    else:
        shared_mem_name = task.shminfo.shm_name

    if type(shared_mem_name) is str:
        shared_mem_name = shared_mem_name.encode()

    total_size = c_size_t(size)
    shm_ret = matrolrtlib.matrolrt_create_shm(total_size,shared_mem_name)
    c = cast(shm_ret,POINTER(MATROLRT_SHM_RET))
    ret = c.contents
    print(ret.shm_desc_ptr,ret.ret)
    if ret.shm_desc_ptr is not None and ret.ret == -errno.EEXIST:
        ret_val = matrolrtlib.matrolrt_shm_bind(ret.shm_desc_ptr,shared_mem_name)
        print(ret_val)
        task.shminfo.create_mode = SHM_CREATE_MODE['BIND']
    else:
        task.shminfo.create_mode = SHM_CREATE_MODE['CREATE']

    if ret.shm_desc_ptr is None:
        print("create shm fail")
    task.shminfo.shm_ret = ret

    shm_ptr = matrolrtlib.matrolrt_shm_alloc(ret.shm_desc_ptr,total_size)
    if shm_ptr is None:
        print(shared_mem_name," alloc fail\n")
    return shm_ptr


def matrolrt_shm_delete(task):
    if(task.shminfo.create_mode == SHM_CREATE_MODE['BIND']):
        print("mode is bind\n");
        ret = matrolrtlib.matrolrt_shm_unbind(task.shminfo.shm_ret.shm_desc_ptr)
        if ret == 0:
            libc.free(pointer(task.shminfo.shm_ret))
            task.shminfo.shm_ret = None
        return ret
    ret = matrolrtlib.matrolrt_shm_delete(task.shminfo.shm_ret.shm_desc_ptr)
    if ret == 0:
        libc.free(pointer(task.shminfo.shm_ret))
        task.shminfo.shm_ret = None
    return ret



#################matrolrt pipe part ###############################

###########pipe is for matrolrt task ipc with linux thread########

def matrolrt_create_pipe(task,size=None,pipe_name=None,mode=LINUX):
    pipe_desc_ptr = None
    shared_pipe_name = None
    ret_val = int(0)
    if pipe_name is not None: #override the shared memory name
        shared_pipe_name = pipe_name
    else:
        shared_pipe_name = task.pipeinfo.pipe_name

    if type(shared_pipe_name) is str:
        shared_pipe_name = shared_pipe_name.encode()

    if mode == MATROLRT:
        total_size = c_size_t(size)
        pipe_ret = matrolrtlib.matrolrt_create_pipe(total_size,shared_pipe_name)
        c = cast(pipe_ret,POINTER(MATROLRT_PIPE_RET))
        ret = c.contents
        print(ret.pipe_desc_ptr,ret.ret)
        if ret.ret < 0:
            print("create pipe fail")
            return task
        task.pipeinfo.pipe_ret = ret

    elif mode == LINUX:
        file_name = b'/proc/xenomai/registry/native/pipes/' + shared_pipe_name
        print(file_name)
        task.pipeinfo.fd = os.open(file_name,os.O_RDWR)
    return task

def matrolrt_pipe_delete(task):
    ret = task.pipeinfo.pipe_ret
    if ret is not None and ret.pipe_desc_ptr is not None:
        ret = matrolrtlib.matrolrt_pipe_delete(ret.pipe_desc_ptr)
        if ret == 0:
            libc.free(pointer(task.pipeinfo.pipe_ret))
            task.pipeinfo.pipe_ret = None
        else:
            print("delete fail\n")
    elif task.pipeinfo.fd is not None:
        os.close(task.pipeinfo.fd)
        task.pipeinfo.fd = None
    return task


def matrolrt_pipe_read(task,buf=None,size=1024,timeout=TM_INFINITE):
    ret = task.pipeinfo.pipe_ret
    if ret is not None and ret.pipe_desc_ptr is not None:
        return matrolrtlib.matrolrt_pipe_read(ret.pipe_desc_ptr,buf,size_t(size),timeout)
    elif task.pipeinfo.fd is not None:
        return  os.read(task.pipeinfo.fd,size)

def matrolrt_pipe_write(task,buf,size=1024,mode=PIPE_NORMAL):
    ret = task.pipeinfo.pipe_ret
    if ret is not None and ret.pipe_desc_ptr is not None:
        return matrolrtlib.matrolrt_pipe_write(ret.pipe_desc_ptr,buf,size_t(size),mode)
    elif task.pipeinfo.fd is not None:
        return os.write(task.pipeinfo.fd,buf)