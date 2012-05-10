import manager
import common
import os
from common import droid

def open_view():
    layout = open(os.path.join(common.path, 'layouts', 'settings.xml'), 'r').read()
    droid.fullShow(layout)
    
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
            #create the seek bar with the current value in for the start value
            current = droid.fullQueryDetail("currentScanInterval").result['text']
            droid.dialogCreateSeekBar(str(current),100,"Scan Interval","How many seconds should the phone wait in between WiFi Scans?  A smaller interval will decrease battery life but increase data collection.")
            droid.dialogSetPositiveButtonText("Update Interval")
            droid.dialogShow()
            sliderResp = droid.dialogGetResponse().result
            currentSliderValue = sliderResp['progress']
            #event=droid.eventWait().result
            #data = event['data']
            #number = data['progress']
            droid.fullSetProperty("currentScanInterval", "text", str(currentSliderValue))
            return manager.EVENT_CONSUME
        elif id == "openThroughputSlider":
            #create the seek bar with the current value in for the start value
            current = droid.fullQueryDetail("currentThroughputInterval").result['text']
            droid.dialogCreateSeekBar(str(current),100,"Throughput Interval","How many seconds should the phone wait in between throughput tests?  A smaller interval will decrease battery life but increase data collection.")
            droid.dialogSetPositiveButtonText("Update Interval")
            droid.dialogShow()
            sliderResp = droid.dialogGetResponse().result
            currentSliderValue = sliderResp['progress']
            #event=droid.eventWait().result
            #data = event['data']
            #number = data['progress']
            droid.fullSetProperty("currentThroughputInterval", "text", str(currentSliderValue))
            return manager.EVENT_CONSUME
        elif id == "minimumBattery":
            #create the seek bar with the current value in for the start value
            current = droid.fullQueryDetail("currentMinimumBattery").result['text']
            droid.dialogCreateSeekBar(str(current),100,"Minimum Battery Level","This app can be configured to stop scanning when battery level is below a certain level.  Choose the minimum battery level.")
            droid.dialogSetPositiveButtonText("Update Minimum battery level")
            droid.dialogShow()
            sliderResp = droid.dialogGetResponse().result
            currentSliderValue = sliderResp['progress']
            #event=droid.eventWait().result
            #data = event['data']
            #number = data['progress']
            droid.fullSetProperty("currentMinimumBattery", "text", str(currentSliderValue)) 
            return manager.EVENT_CONSUME
    elif event["name"]=="screen":
        if event["data"]=="destroy":
            manager.close_app()
            return manager.EVENT_CONSUME
    elif event["name"] == "EXIT_APP":
        manager.close_app()
    
    return manager.EVENT_UNUSED