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
        
        if event["name"]=="click":
            id = event["data"]["id"]
        else:
            continue # for now
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
        elif id == "button2":
            droid.fullSetProperty("editText1","text","OK has been pressed")
        elif id=="button1":
            droid.fullSetProperty("textView1","text","Other stuff here")
            print droid.fullSetProperty("background","backgroundColor","0xff7f0000")
        elif event["name"]=="screen":
            if event["data"]=="destroy":
                return
        elif event["name"] == "EXIT_APP":
            return
        elif id == "exitButton":
            return


if __name__ == '__main__':
    if len(sys.argv) == 3:
        addr = sys.argv[1], sys.argv[2]
        droid = sl4a.Android(addr)
    else:
        droid = sl4a.Android()
    common.droid = droid
    common.path = path
    
    # Turn on GPS at app startup
    common.gps_lock()
    
    layout = open(os.path.join(path, 'layouts', 'main.xml'), 'r').read()
    droid.fullShow(layout)
    
    droid.addOptionsMenuItem("Close Application","EXIT_APP",None,"star_on")
    info = droid.wifiGetConnectionInfo().result
    print info
    if 'ssid' in info.keys():
        droid.fullSetProperty("currentNetworkSSID", "text", "Current WiFi Network SSID: " + droid.wifiGetConnectionInfo().result['ssid'])
    else:
        droid.fullSetProperty("currentNetworkSSID", "text", "Current WiFi Network SSID: NOT CONNECTED or CARD DISABLED")
    
    event_loop()
    droid.fullDismiss()