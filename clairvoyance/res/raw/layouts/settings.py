import manager
import common
import os
import json
from common import droid, default_settings


MINIMUM_UPDATE = 15

def save_settings():
    droid.fullSetProperty("currentScanInterval", "text", str(settings['scan_interval']) + ' seconds')
    droid.fullSetProperty("currentMinimumBattery", "text", str(settings['minimum_battery']) + "%")       
    droid.fullSetProperty("bufferSize", "text", str(settings['buffer_size']))       
    droid.prefPutValue('settings', json.dumps(settings), 'clairvoyance')

def open_view():
    global settings
    layout = open(os.path.join(common.path, 'layouts', 'settings.xml'), 'r').read()
    droid.fullShow(layout)
    
    prefs = droid.prefGetValue('settings', 'clairvoyance').result
    if prefs is not None:
        settings = json.loads(prefs)
    else:
        settings = common.default_settings
    save_settings() # Updates the UI, and places the defaults in the keystore if nothing was loaded
    droid.clearOptionsMenu()  
    droid.addOptionsMenuItem("Close Application","EXIT_APP",None,"ic_menu_close_clear_cancel")
    info = droid.wifiGetConnectionInfo().result
    if 'ssid' in info.keys():
        droid.fullSetProperty("currentNetworkSSID", "text", "Current WiFi Network SSID: " + droid.wifiGetConnectionInfo().result['ssid'])
    else:
        droid.fullSetProperty("currentNetworkSSID", "text", "Current WiFi Network SSID: NOT CONNECTED or CARD DISABLED")
    

def close_view():
    droid.fullDismiss()


def handle_event(event):
    """
    This should handle events one at a time. It should return a manager.EVENT_*
    constant.
    """
    if event["name"]=="click":
        id = event["data"]["id"]
        if id == "openScanSlider":
            print settings
            print type(settings)
            print settings['scan_interval']
            droid.dialogCreateSeekBar(settings['scan_interval'], 120, "Scan Interval", "How many seconds should the phone wait in between WiFi Scans?  A smaller interval will decrease battery life but increase data collection.")
            droid.dialogSetPositiveButtonText("Update Interval")
            droid.dialogShow()
            sliderResp = droid.dialogGetResponse().result
            valToSet = sliderResp['progress']
            if valToSet <= MINIMUM_UPDATE: valToSet = MINIMUM_UPDATE
            settings['scan_interval'] = valToSet
            save_settings()
            return manager.EVENT_CONSUME
        elif id == "minimumBattery":
            droid.dialogCreateSeekBar(str(settings['minimum_battery']), 80, "Minimum Battery Level", "This app can be configured to stop scanning when battery level is below a certain level.  Choose the minimum battery level.")
            droid.dialogSetPositiveButtonText("Update Minimum battery level")
            droid.dialogShow()
            sliderResp = droid.dialogGetResponse().result
            valToSet = sliderResp['progress']
            if valToSet == 0: valToSet = 1
            settings['minimum_battery'] = valToSet
            save_settings()
            return manager.EVENT_CONSUME
        elif id == "bufferSizeSlider":
              droid.dialogCreateSeekBar(str(settings['buffer_size']), 50, "Buffer Size", "How often should the app send its collected data to the server?  Decreasing this size will send data to the server more often (though the same amount of total data will be sent).")
              droid.dialogSetPositiveButtonText("Update Buffer Limit")
              droid.dialogShow()
              sliderResp = droid.dialogGetResponse().result
              valToSet = sliderResp['progress']
              if valToSet == 0: valToSet = 1
              settings['buffer_size'] = valToSet
              save_settings()
              return manager.EVENT_CONSUME
        
    elif event["name"] == "key":
        id = event["data"]["key"]
        #BACK_BUTTON = '4'
        if id == '4':
            #the back button was pressed
            print "BACK BUTTON PRESSED!!!"
            manager.pop_view();
    elif event["name"]=="screen":
        if event["data"]=="destroy":
            pass
            #manager.close_app()
            #return manager.EVENT_CONSUME
    elif event["name"] == "EXIT_APP":
        droid.stopLocating()
        manager.close_app()
    elif event["name"] == "SAVE_SETTINGS":
        save_settings()
    else:
        print "Unused event in settings."
        return manager.EVENT_UNUSED
