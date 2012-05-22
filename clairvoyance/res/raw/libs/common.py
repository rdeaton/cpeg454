import os

# Holds the instance of the Android object
droid = None
# Holds the path to the base directory
path = ''
# DNS name of server to report to (no HTTP, url, etc)
server='localhost:5050'
gps_locked = False

views = {}

def load_views():
    for f in os.listdir(os.path.join(path, 'layouts')):
        if f[-3:] == '.py' and f != "__init__.py":
            views[f[:-3]] = __import__('layouts.' + f[:-3], fromlist=["*"])
    
def gps_is_enabled():
    if 'gps' not in droid.locationProviders().result:
        # Wat? No GPS?
        return False
    return droid.locationProviderEnabled('gps').result

def open_gps_settings():
    intent = droid.makeIntent(None, None, None, None, None, "com.android.settings", "com.android.settings.SecuritySettings", 0).result
    droid.startActivityForResultIntent(intent)

def gps_prompt():
    droid.dialogCreateAlert("GPS is not currently enabled. Enable it now?")
    droid.dialogSetPositiveButtonText("Yes")
    droid.dialogSetNegativeButtonText("No")
    droid.dialogShow()
    response = droid.dialogGetResponse().result
    droid.dialogDismiss()
    if 'which' in response and response['which'] == 'positive':
        open_gps_settings()
        return gps_is_enabled()
    else:
        return False

def gps_lock(prompt = True, mSecondsToWaitOnLock = 30000, minUpdateDistance = 30):
    """
    Attempts to enable the GPS sensor. If prompt is false, it will pull up the
    settings pane without asking if GPS is off on the first attempt to enable.
    """
    global gps_locked
    error = "Could not get a GPS lock at this time."
    if not gps_is_enabled():
        if not gps_prompt():
            droid.makeToast("1" + error)
            return False
        
    # Let's make sure GPS is on
    droid.dialogCreateSpinnerProgress("Clairvoyance", "Waiting for GPS...")
    droid.dialogShow()
    droid.startLocating(mSecondsToWaitOnLock, minUpdateDistance)
    count = 0
    while count < 2:
        droid.eventWaitFor('location', 15000)
        droid.eventClearBuffer()
    
        location = droid.readLocation().result
        if location == {} or 'gps' not in location:
            count += 1
        else:
            droid.dialogDismiss()
            gps_locked = True
            return True
    droid.dialogDismiss()
    droid.makeToast(error)
    gps_locked = False
    return False