from ctypes import *
from ctypes.util import find_library


libnative_name = '/usr/xenomai/lib/libnative.so'
libxenomai_name = '/usr/xenomai/lib/libxenomai.so'


xenomailib = CDLL(libxenomai_name,mode=RTLD_GLOBAL) #add mode to fix xeno_* symbol cannot be find issue

#print (find_library('xeno_current_mode_key'))
nativelib = CDLL(libnative_name,mode=RTLD_GLOBAL)

def test():
    print ('test')