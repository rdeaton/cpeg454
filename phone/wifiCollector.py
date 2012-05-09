import android
droid=android.Android()

def eventloop():
    while True:
        event=droid.eventWait().result
        
        if event["name"]=="click":
            id=event["data"]["id"]
	    if id=="openScanSlider":
                #create the seek bar with the current value in for the start value
                print droid.fullQueryDetail("currentScanInterval")
	        droid.dialogCreateSeekBar(10,100,"Scan Interval","How many seconds should the phone wait in between WiFi Scans?  A smaller interval will decrease battery life but increase data collection.")
                droid.dialogSetPositiveButtonText("Update Interval")
                droid.dialogShow()
                sliderResp = droid.dialogGetResponse().result
                currentSliderValue = sliderResp['progress']
                #event=droid.eventWait().result
                #data = event['data']
                #number = data['progress']
                droid.fullSetProperty("currentScanInterval", "text", str(currentSliderValue))
            if id=="openThroughputSlider":
                #create the seek bar with the current value in for the start value
	        droid.dialogCreateSeekBar(10,100,"Throughput Interval","How many seconds should the phone wait in between throughput tests?  A smaller interval will decrease battery life but increase data collection.")
                droid.dialogSetPositiveButtonText("Update Interval")
                droid.dialogShow()
                sliderResp = droid.dialogGetResponse().result
                currentSliderValue = sliderResp['progress']
                #event=droid.eventWait().result
                #data = event['data']
                #number = data['progress']
                droid.fullSetProperty("currentThroughputInterval", "text", str(currentSliderValue))
            if id=="exitButton":
                return
            elif id=="button2":
                droid.fullSetProperty("editText1","text","OK has been pressed")
            elif id=="button1":
                droid.fullSetProperty("textView1","text","Other stuff here")
                print droid.fullSetProperty("background","backgroundColor","0xff7f0000")
            elif event["name"]=="screen":
                if event["data"]=="destroy":
                    return
        elif event["name"] == "EXIT_APP":
            return
            

print "Started"
layout="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
        android:id="@+id/background"
        android:orientation="vertical" android:layout_width="match_parent"
        android:layout_height="match_parent" android:background="#ff000000">


        <CheckBox android:layout_height="wrap_content" android:id="@+id/scanEnable" android:layout_width="234dp" android:text="Enable Scan Tests?" android:checked="true"></CheckBox>   
        <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:id="@+id/linearLayout2">
	    <Button android:id="@+id/openScanSlider" android:layout_width="wrap_content"
                    android:layout_height="wrap_content" android:text="Change Scan Interval"></Button>            
            <TextView android:layout_width="match_parent"
                    android:layout_height="wrap_content" android:text="20"
                    android:id="@+id/currentScanInterval" android:textAppearance="?android:attr/textAppearanceLarge" android:gravity="right"></TextView>
        </LinearLayout>

        <CheckBox android:layout_height="wrap_content" android:id="@+id/throughputEnable" android:layout_width="234dp" android:text="Enable Throughput Tests?" android:checked="true"></CheckBox>
        <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:id="@+id/linearLayout3">
	    <Button android:id="@+id/openThroughputSlider" android:layout_width="wrap_content"
                    android:layout_height="wrap_content" android:text="Change Throughput Test Interval"></Button>            
            <TextView android:layout_width="match_parent"
                    android:layout_height="wrap_content" android:text="30"
                    android:id="@+id/currentThroughputInterval" android:textAppearance="?android:attr/textAppearanceLarge" android:gravity="right"></TextView>
        </LinearLayout>


		 
</LinearLayout>
"""
droid.addOptionsMenuItem("Close Application","EXIT_APP",None,"star_on")
#print layout
print droid.fullShow(layout)
eventloop()
#print droid.fullQuery()
#print "Data entered =",droid.fullQueryDetail("editText1").result
droid.fullDismiss()


'''
FROM THE TOP OF THE LAYOUT
        <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:id="@+id/linearLayout1">
                <Button android:id="@+id/button1" android:layout_width="wrap_content"
                        android:layout_height="wrap_content" android:text="Test 1"></Button>
                <Button android:id="@+id/button2" android:layout_width="wrap_content"
                        android:layout_height="wrap_content" android:text="Ok"></Button>
                <Button android:id="@+id/button3" android:layout_width="wrap_content"
                        android:layout_height="wrap_content" android:text="Cancel"></Button>
        </LinearLayout>
'''

'''
FROM THE BOTTOM OF THE LAYOUT
        <EditText android:layout_width="match_parent"
                android:layout_height="wrap_content" android:id="@+id/editText1"
                android:tag="Tag Me" android:inputType="number">
                <requestFocus></requestFocus>
        </EditText>
'''
