import manager
import common
import os
import json
import checkin
from common import droid, default_settings


SSIDS_TO_TRACK = ["UDel", "UDel Secure", "acad"]

def open_view():
    layout = open(os.path.join(common.path, 'layouts', 'collectData.xml'), 'r').read()
    droid.fullShow(layout)

    #set the text fields
    prefs = droid.prefGetValue('settings', 'clairvoyance').result
    if prefs is not None:
        settings = json.loads(droid.prefGetValue('settings','clairvoyance').result)
    else:
        settings = commonn.default_settings
    
    droid.fullSetProperty("scanInterval", "text", "Current scan interval: " + str(settings['scan_interval']))
    droid.fullSetProperty("throughputInterval", "text", "Current throughput interval: " + str(settings['throughput_interval']))
    droid.fullSetProperty("minimumBattery", "text", "Current minimum battery cutoff: " + str(settings['minimum_battery']))
    droid.fullSetProperty("bufferSize", "text", "Current buffer size: " + str(settings['buffer_size']))
    currentAP = droid.wifiGetConnectionInfo().result
    print currentAP['network_id']
    if currentAP['network_id'] != -1:
        droid.fullSetProperty("currentNetworkSSID", "text", "Current WiFi Network SSID:" + currentAP['ssid'])
    else:
        droid.fullSetProperty("currentNetworkSSID", "text", "Current WiFi Network SSID:" + " NOT CONNECTED")
    
    
    droid.clearOptionsMenu()  
    droid.addOptionsMenuItem("Close Application","EXIT_APP",None,"star_on")

    #start the gps with the interval that the user has specified in his or her frequency setting
    has_gps_lock = common.gps_lock(mSecondsToWaitOnLock = settings['scan_interval'] * 1000, minUpdateDistance = 1)
    
    if has_gps_lock:
        droid.fullSetProperty("status", "text", "GPS LOCK ACQUIRED")
    else:
        droid.fullSetProperty("status", "text", "NO GPS LOCK")

    handle_event.bufferCounter = 0
    handle_event.location = []
    handle_event.JSON_sends = 0
    handle_event.odd = False
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
            return manager.EVENT_CONSUME
    elif event["name"]=="screen":
        if event["data"]=="destroy":
            pass
            #manager.close_app()
            return manager.EVENT_USED
    elif event["name"] == "EXIT_APP":
        manager.close_app()
        return manager.EVENT_CONSUME
    elif event["name"] == "SAVE_SETTINGS":
        save_settings()
        return manager.EVENT_USED
    elif event["name"] == "location":
        print "GOT LOC!"    

        loc_data = droid.readLocation().result
        myLat = loc_data['gps']['latitude']
        myLong = loc_data['gps']['longitude']
        accuracy = loc_data['gps']['accuracy']
        myID = droid.getDeviceId().result
        networks = droid.wifiGetScanResults().result
        if networks != None and handle_event.odd == False:
            handle_event.odd = True
            handle_event.odd = True
            for singleNetwork in networks:
                if singleNetwork['ssid'] not in SSIDS_TO_TRACK:
                    handle_event.bufferCounter = handle_event.bufferCounter + 1
                    handle_event.location.append(checkin.create_checkin(phone_id = myID , latitude = myLat , longitude = myLong, bssid = singleNetwork['bssid'], ssid = singleNetwork['ssid'] , signal = singleNetwork['level'] , performance = accuracy))
        else:
            handle_event.odd = False
            
        settings = json.loads(droid.prefGetValue('settings','clairvoyance').result)    
        if (handle_event.bufferCounter >= settings['buffer_size']):
            try:
                checkin.send_checkins(handle_event.location)
            except Exception:
                droid.makeToast("Server did not acknowledge receipt of object.")
                
            handle_event.location = []
            handle_event.bufferCounter = 0
            handle_event.JSON_sends += 1
        
        droid.fullSetProperty("status", "text", "Number of reads: " + str(handle_event.bufferCounter) + " Number of JSON sends:" + str(handle_event.JSON_sends) )
      
        return manager.EVENT_CONSUME
    else:
        print "Unused event in collectData."
        return manager.EVENT_UNUSED
        
