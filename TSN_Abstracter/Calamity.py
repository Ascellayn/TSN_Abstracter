"""
This module will make every Python developer cry.  
Enforces even more strict typing by using and replacing certain data types with ctype variants.  
This module is NOT recommended to import unless you ABSOLUTELY ARE 100% SURE YOU KNOW WHAT YOU ARE DOING!  
"""
from ctypes import pointer as ptr;
from ctypes import sizeof;



from ctypes import c_bool as bool;
from ctypes import c_char as char;
from ctypes import c_float as float;
from ctypes import c_double as double;


from ctypes import c_int as int;
from ctypes import c_int8 as int8_t;
from ctypes import c_int16 as int16_t;
from ctypes import c_int32 as int32_t;
from ctypes import c_int64 as int64_t;


from ctypes import c_uint as uint;
from ctypes import c_uint8 as uint8_t;
from ctypes import c_uint16 as uint16_t;
from ctypes import c_uint32 as uint32_t;
from ctypes import c_uint64 as uint64_t;


from ctypes import c_long as long;
from ctypes import c_ulong as ulong;

from ctypes import c_longlong as longlong;
from ctypes import c_ulonglong as ulonglong;

true: bool = bool(True);
false: bool = bool(False);

__all__: list[str] = [
	"ptr", "sizeof",
	"bool", "char", "float", "double",
	"int", "int8_t", "int16_t", "int32_t", "int64_t",
	"uint", "uint8_t", "uint16_t", "uint32_t", "uint64_t",
	"long", "ulong", "longlong", "ulonglong",
	"true", "false"
]