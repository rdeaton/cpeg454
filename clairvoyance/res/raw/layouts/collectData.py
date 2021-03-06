import manager
import common
import os
import json
import checkin
from common import droid, default_settings, SSIDS_TO_TRACK


def open_view():
    layout = open(os.path.join(common.path, 'layouts', 'collectData.xml'), 'r').read()
    droid.fullShow(layout)

    #set the text fields
    prefs = droid.prefGetValue('settings', 'clairvoyance').result
    if prefs is not None:
        settings = json.loads(droid.prefGetValue('settings','clairvoyance').result)
    else:
        settings = common.default_settings
    
    droid.fullSetProperty("scanInterval", "text", "Scan interval: " + str(settings['scan_interval']) + " seconds")
    droid.fullSetProperty("minimumBattery", "text", "Minimum battery cutoff: " + str(settings['minimum_battery']) + "%")
    droid.fullSetProperty("bufferSize", "text", "Buffer limit: " + str(settings['buffer_size']))
    currentAP = droid.wifiGetConnectionInfo().result
    print currentAP['network_id']
    if currentAP['network_id'] != -1:
        droid.fullSetProperty("currentNetworkSSID", "text", "Current WiFi Network SSID:" + currentAP['ssid'])
    else:
        droid.fullSetProperty("currentNetworkSSID", "text", "Current WiFi Network SSID:" + " NOT CONNECTED")
    
    
    droid.clearOptionsMenu()  
    droid.addOptionsMenuItem("Close Application","EXIT_APP",None,"ic_menu_close_clear_cancel")

    #start the gps with the interval that the user has specified in his or her frequency setting
    has_gps_lock = common.gps_lock(mSecondsToWaitOnLock = settings['scan_interval'] * 1000, minUpdateDistance = 1)
    #start battery monitoring
    droid.batteryStartMonitoring()
    if has_gps_lock:
        droid.fullSetProperty("status", "text", "GPS LOCK ACQUIRED")
    else:
        droid.fullSetProperty("status", "text", "NO GPS LOCK")

    handle_event.bufferCounter = 0
    handle_event.totalPointsCollected = 0
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
            droid.stopLocating()
            manager.pop_view();
            return manager.EVENT_CONSUME
    elif event["name"]=="screen":
        if event["data"]=="destroy":
            pass
            #manager.close_app()
            return manager.EVENT_USED
    elif event["name"] == "EXIT_APP":
        droid.stopLocating()
        manager.close_app()
        return manager.EVENT_CONSUME
    elif event["name"] == "SAVE_SETTINGS":
        save_settings()
        return manager.EVENT_USED
    elif event["name"] == "battery":
        #if battery level is below the minimum, then stop locating and set the low battery warning!
        prefs = droid.prefGetValue('settings', 'clairvoyance').result
        if prefs is not None:
            settings = json.loads(droid.prefGetValue('settings','clairvoyance').result)
        else:
            settings = common.default_settings
        if (droid.batteryGetLevel().result < int(settings['minimum_battery'])):
            droid.stopLocating()
            droid.fullSetProperty("status", "text", "Battery level too low.  Please charge the device and try again (or change the minimum battery level in settings)." )

    elif event["name"] == "location":
        loc_data = droid.readLocation().result
        
        try:
            myLat = loc_data['gps']['latitude']
            myLong = loc_data['gps']['longitude']
            accuracy = loc_data['gps']['accuracy']
            
            if droid.checkWifiState().result == False:
                droid.makeToast("WiFi was not enabled.  Enabling WiFi...")
                droid.toggleWifiState(True)
                                
            myID = droid.getDeviceId().result
            networks = droid.wifiGetScanResults().result
            if networks != None and handle_event.odd == False:
                handle_event.odd = True
                for singleNetwork in networks:
                    if singleNetwork['ssid'] in common.SSIDS_TO_TRACK:
                        handle_event.totalPointsCollected += 1
                        handle_event.bufferCounter = handle_event.bufferCounter + 1
                        handle_event.location.append(checkin.create_checkin(phone_id = myID , latitude = myLat , longitude = myLong, bssid = singleNetwork['bssid'], ssid = singleNetwork['ssid'] , signal = singleNetwork['level'] , performance = accuracy))
            elif networks != None:
                handle_event.odd = False

            
            settings = json.loads(droid.prefGetValue('settings','clairvoyance').result)
            
            if (handle_event.bufferCounter >= settings['buffer_size'] and handle_event.odd == True):
                try:
                    checkin.send_checkins(handle_event.location)
                    handle_event.location = []
                    handle_event.bufferCounter = 0
                    handle_event.JSON_sends += 1
                    
                except Exception,e:
                    droid.makeToast("Error: " + str(e))
                    
            
            droid.fullSetProperty("status", "text", "Total number of data points collected: " + str(handle_event.totalPointsCollected) + "\nCurrent buffer size: " + str(handle_event.bufferCounter) + "\nNumber of JSON sends to server: " + str(handle_event.JSON_sends) )
            
            

        except Exception:
            droid.fullSetProperty("status", "text", "NO GPS LOCK")
        return manager.EVENT_CONSUME
    else:
        print "Unused event in collectData."
        return manager.EVENT_UNUSED
        
