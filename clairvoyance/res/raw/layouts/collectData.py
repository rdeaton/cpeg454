import manager
import common
import os
import json
from common import droid

settings = {
     'scan_interval' : 60,
     'throughput_interval' : 60,
     'minimum_battery' : 15,
     'buffer_size' : 5}



def open_view():
    global settings
    layout = open(os.path.join(common.path, 'layouts', 'collectData.xml'), 'r').read()
    droid.fullShow(layout)

    #set the text fields
    droid.fullSetProperty("scanInterval", "text", "Current scan interval: " + str(settings['scan_interval']))
    droid.fullSetProperty("throughputInterval", "text", "Current throughput interval: " + str(settings['throughput_interval']))
    droid.fullSetProperty("minimumBattery", "text", "Current minimum battery cutoff: " + str(settings['minimum_battery']))
    droid.fullSetProperty("bufferSize", "text", "Current buffer size: " + str(settings['buffer_size']))
    droid.fullSetProperty("currentNetworkSSID", "text", "Current WiFi Network SSID:" + droid.wifiGetConnectionInfo().result['ssid'])
    
    
    
    droid.clearOptionsMenu()  
    droid.addOptionsMenuItem("Close Application","EXIT_APP",None,"star_on")

    

def close_view():
    droid.fullDismiss()


def handle_event(event):
    """
    This should handle events one at a time. It should return a manager.EVENT_*
    constant.
    """
    if event["name"] == "key":
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
        return manager.EVENT_UNUSED
