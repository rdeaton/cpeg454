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
        time.sleep(5)
        return

if __name__ == '__main__':
    if len(sys.argv) == 3:
        addr = sys.argv[1], sys.argv[2]
        droid = sl4a.Android(addr)
    else:
        droid = sl4a.Android()
    common.droid = droid
    common.path = path

    layout = open(os.path.join(path, 'layouts', 'main.xml'), 'r').read()
    droid.fullShow(layout)
    
    # Let's make sure GPS is on
    droid.startLocating()
    droid.eventWaitFor('location')
    
    location = droid.readLocation().result
    if location == {} or 'gps' not in location:
        # We couldn't track the location
        droid.dialogCreateAlert("GPS is not current enabled. Enable it now?")
        droid.setPositiveButtonText("Yes")
        droid.setNegativeButtonText("No")
        droid.dialogShow()
        
        droid.eventWaitFor('dialog')
    
    
    
    
    intent = droid.makeIntent(None, None, None, None, None, "com.android.settings", "com.android.settings.SecuritySettings", 0).result
    droid.startActivityForResultIntent(intent)
    
    
    
    
    event_loop()
    droid.fullDismiss()