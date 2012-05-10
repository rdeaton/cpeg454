import time
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + '/libs')
import fix_json
try:
    import android as sl4a
except ImportError:
    import sl4a

if __name__ == '__main__':
    import common
    if len(sys.argv) == 3:
        addr = sys.argv[1], sys.argv[2]
        droid = sl4a.Android(addr)
    else:
        droid = sl4a.Android()
    common.droid = droid
    common.path = path
    common.load_views()
    import manager
    
    
    manager.push_view(common.views['settings'])
    
    manager.main_loop()
    
    # Turn on GPS at app startup
    common.gps_lock()
    
