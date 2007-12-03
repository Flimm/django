import os, sys
from ctypes import CDLL, string_at
from ctypes.util import find_library
from django.contrib.gis.gdal.error import OGRException

# Custom library path set?
try:
    from django.conf import settings
    lib_name = settings.GDAL_LIBRARY_PATH
except (AttributeError, EnvironmentError):
    lib_name = None

if lib_name:
    pass
elif os.name == 'nt':
    # Windows NT shared library
    lib_name = 'libgdal-1.dll'
    errcheck_flag = False
elif os.name == 'posix':
    platform = os.uname()[0]
    if platform == 'Darwin':
        # Mac OSX shared library
        lib_name = 'libgdal.dylib'
    else: 
        # Attempting to use .so extension for all other platforms.
        lib_name = 'libgdal.so'
    errcheck_flag = True
else:
    raise OGRException('Unsupported OS "%s"' % os.name)

# This loads the GDAL/OGR C library
lgdal = CDLL(lib_name)

#### Version-information functions. ####
def _version_info(key):
    "Returns GDAL library version information with the given key."
    buf = lgdal.GDALVersionInfo(key)
    if buf: return string_at(buf)

def gdal_version():
    "Returns only the GDAL version number information."
    return _version_info('RELEASE_NAME')

def gdal_full_version(): 
    "Returns the full GDAL version information."
    return _version_info('')

def gdal_release_date(date=False): 
    """
    Returns the release date in a string format, e.g, "2007/06/27".
    If the date keyword argument is set to True, a Python datetime object
    will be returned instead.
    """
    from datetime import datetime
    rel = _version_info('RELEASE_DATE')
    yy, mm, dd = map(int, (rel[0:4], rel[4:6], rel[6:8]))
    d = datetime(yy, mm, dd)
    if date: return d
    else: return d.strftime('%Y/%m/%d')
