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
import common
    
def event_loop():
    while True:
        event = droid.eventWait().result
        print event
        # droid.fullQueryDetail("textview1").result['text'] = str(event)
        time.sleep(1)
        return

if __name__ == '__main__':
    if len(sys.argv) == 3:
        addr = sys.argv[1], sys.argv[2]
        droid = sl4a.Android(addr)
    else:
        droid = sl4a.Android()
    common.droid = droid
    common.path = path
    
    common.try_to_enable_gps()
    
    
    
    layout = open(os.path.join(path, 'layouts', 'main.xml'), 'r').read()
    droid.fullShow(layout)
    
    event_loop()
    droid.fullDismiss()