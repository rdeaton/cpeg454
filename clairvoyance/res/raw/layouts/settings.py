import manager
import common
import os
import json
from common import droid

settings = {
     'scan_interval' : 60,
     'throughput_interval' : 60,
     'minimum_battery' : 15}

def save_settings():
    droid.fullSetProperty("currentScanInterval", "text", str(settings['scan_interval']) + 's')
    droid.fullSetProperty("currentThroughputInterval", "text", str(settings['throughput_interval']) + 's')
    droid.fullSetProperty("currentMinimumBattery", "text", str(settings['minimum_battery']) + '%')     
    droid.prefPutValue('settings', json.dumps(settings), 'clairvoyance')

def open_view():
    global settings
    layout = open(os.path.join(common.path, 'layouts', 'settings.xml'), 'r').read()
    droid.fullShow(layout)
    
    prefs = droid.prefGetValue('settings', 'clairvoyance').result
    if prefs is not None:
        settings = json.loads(prefs)
    save_settings() # Updates the UI, and places the defaults in the keystore if nothing was loaded
    
    droid.addOptionsMenuItem("Save Settings","SAVE_SETTINGS",None,"star_on")    
    droid.addOptionsMenuItem("Close Application","EXIT_APP",None,"star_on")
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
            droid.dialogCreateSeekBar(settings['scan_interval'], 100, "Scan Interval", "How many seconds should the phone wait in between WiFi Scans?  A smaller interval will decrease battery life but increase data collection.")
            droid.dialogSetPositiveButtonText("Update Interval")
            droid.dialogShow()
            sliderResp = droid.dialogGetResponse().result
            settings['scan_interval'] = sliderResp['progress']
            save_settings()
            return manager.EVENT_CONSUME
        elif id == "openThroughputSlider":
            droid.dialogCreateSeekBar(str(settings['throughput_interval']), 100, "Throughput Interval", "How many seconds should the phone wait in between throughput tests?  A smaller interval will decrease battery life but increase data collection.")
            droid.dialogSetPositiveButtonText("Update Interval")
            droid.dialogShow()
            sliderResp = droid.dialogGetResponse().result
            settings['throughput_interval'] = sliderResp['progress']
            save_settings()
            return manager.EVENT_CONSUME
        elif id == "minimumBattery":
            droid.dialogCreateSeekBar(str(settings['minimum_battery']), 100, "Minimum Battery Level", "This app can be configured to stop scanning when battery level is below a certain level.  Choose the minimum battery level.")
            droid.dialogSetPositiveButtonText("Update Minimum battery level")
            droid.dialogShow()
            sliderResp = droid.dialogGetResponse().result
            settings['minimum_battery'] = sliderResp['progress']
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
        manager.close_app()
    elif event["name"] == "SAVE_SETTINGS":
        save_settings()
    else:
        print "XX" + event["name"] + "XX"
        print type(event["name"])
        print event["data"]["key"]
        print type(event["data"]["key"])
    return manager.EVENT_UNUSED
