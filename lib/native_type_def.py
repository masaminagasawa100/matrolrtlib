from ctypes import *

H_MAPPABLE =  0x200
H_SINGLE  =  0x400
H_SHARED  =  (H_MAPPABLE|H_SINGLE)

xnhandle_t = c_ulong
caddr_t = c_char_p
size_t = c_ulong
RTIME = c_ulonglong

class MATROLRT_SHM_RET(Structure):
    _fields_ = [
    ('shm_desc_ptr',c_void_p),
	('ret',c_int)
    ]

class MATROLRT_PIPE_RET(Structure):
    _fields_ = [
    ('pipe_desc_ptr',c_void_p),
	('ret',c_int)
    ]


SHM_CREATE_MODE = {
    'NONE':0,
    'BIND':1,
    'CREATE':2
}


matrolrttaskentrytype = CFUNCTYPE(None,c_void_p)


class taskinfo():
    def __init__(self,name,func,args):
        if type(name) is str:
            self.name = name.encode()
        else:
            self.name = name
        self.entry = matrolrttaskentrytype(func)
        self.args = pointer(args)
        self.ptr = None # this is for matrolrt task ptr when we need delete the task

class shminfo():
    def __init__(self,name):
        if type(name) is str:
            self.shm_name = name.encode() + b'_shm'
        else:
            self.shm_name = name + b'_shm'
        self.shm_ret = None
        self.create_mode = SHM_CREATE_MODE['NONE']

class pipeinfo():
    def __init__(self,name):
        if type(name) is str:
            self.pipe_name = name.encode() + b'_pipe'
        else:
            self.pipe_name = name + b'_pipe'
        self.pipe_ret = None
        self.fd = None

class matrolrttask():
    def __init__(self,name,func,args):
        self.taskinfo = taskinfo(name,func,args)
        self.shminfo  = shminfo(name)
        self.pipeinfo = pipeinfo(name)



TM_INFINITE = RTIME(0)
TM_NONBLOCK = RTIME(-1)

PIPE_NORMAL = c_int(0)
PIPE_URGENT = c_int(1)

LINUX    = 0
MATROLRT = 1

