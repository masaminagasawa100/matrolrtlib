from ctypes import *
from ctypes.util import find_library


libnative_name = '/usr/xenomai/lib/libnative.so'
libxenomai_name = '/usr/xenomai/lib/libxenomai.so'
libmatrolrt_name = '../c_lib/libmatrolrt.so'


#xenomailib = CDLL(libxenomai_name,mode=RTLD_GLOBAL) #add mode to fix xeno_* symbol cannot be find issue

#nativelib = CDLL(libnative_name,mode=RTLD_GLOBAL)

matrolrtlib = CDLL(libmatrolrt_name)