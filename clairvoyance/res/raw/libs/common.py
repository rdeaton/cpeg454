# Holds the instance of the Android object
droid = None
# Holds the path to the base directory
path = ''
# Holds the current state of the GPS sensor
gps_enabled = None

def try_to_enable_gps(prompt = True):
    """
    Attempts to enable the GPS sensor. If prompt is false, it will pull up the
    settings pane without asking if GPS is off on the first attempt to enable.
    """
    global gps_enabled
    while True:
        # Let's make sure GPS is on
        droid.dialogCreateSpinnerProgress("Clairvoyance", "Waiting for GPS...")
        droid.dialogShow()
        droid.startLocating()
        droid.eventWaitFor('location')
        droid.dialogDismiss()
    
        location = droid.readLocation().result
        if location == {} or 'gps' not in location:
            # We couldn't track the location
            if prompt:
                droid.dialogCreateAlert("GPS is not currently enabled. Enable it now?")
                droid.dialogSetPositiveButtonText("Yes")
                droid.dialogSetNegativeButtonText("No")
                droid.dialogShow()
                response = droid.dialogGetResponse().result
                if 'which' in response and response['which'] == 'positive':
                    intent = droid.makeIntent(None, None, None, None, None, "com.android.settings", "com.android.settings.SecuritySettings", 0).result
                    droid.startActivityForResultIntent(intent)
                else:
                    droid.stopLocating()
                    gps_enabled = False
                    return False
            else:
                intent = droid.makeIntent(None, None, None, None, None, "com.android.settings", "com.android.settings.SecuritySettings", 0).result
                droid.startActivityForResultIntent(intent)
                prompt = True
        
        else:
            droid.stopLocating()
            gps_enabled = True
            return True