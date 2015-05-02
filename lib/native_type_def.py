from ctypes import *

H_MAPPABLE =  0x200
H_SINGLE  =  0x400
H_SHARED  =  (H_MAPPABLE|H_SINGLE)

xnhandle_t = c_ulong
caddr_t = c_char_p
size_t = c_ulong
RTIME = c_ulonglong

class RT_HEAP_PLACEHOLDER(Structure):
    _fields_ = [

    ('opaque',xnhandle_t),
	('opaque2',c_void_p),
    ('mapbase',caddr_t),
	('mapsize',size_t),
    ('area',c_ulong)
    ]
RT_HEAP =  RT_HEAP_PLACEHOLDER



XENO_TASK_MAGIC = 0x55550101



