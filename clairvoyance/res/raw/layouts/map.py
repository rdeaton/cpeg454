import manager
import common
import os
import json
import checkin
from common import droid, default_settings, SSIDS_TO_TRACK


def open_view():
    #load the layout
    
    #create the menu button buttons
    droid.clearOptionsMenu()  
    droid.addOptionsMenuItem("Low Signal Strength","GET_LOW",None,"star_on")
    droid.addOptionsMenuItem("Medium Signal Strength","GET_MED",None,"star_on")
    droid.addOptionsMenuItem("High Signal Strength","GET_HIGH",None,"star_on")
    droid.addOptionsMenuItem("Close Application","EXIT_APP",None,"star_on")
    
    droid.webViewShow(os.path.join(common.path, 'layouts', 'map.html')) 
    
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
    elif event["name"] == "GET_LOW":
        droid.webViewShow("http://107.20.202.68:5052/static/bad.html") 
        return manager.EVENT_CONSUME
    elif event["name"] == "GET_MED":
        droid.webViewShow("http://107.20.202.68:5052/static/medium.html") 
        return manager.EVENT_CONSUME
    elif event["name"] == "GET_HIGH":
        droid.webViewShow("http://107.20.202.68:5052/static/good.html") 
        return manager.EVENT_CONSUME
        
    else:
        print "Unused event in collectData."
        return manager.EVENT_UNUSED
        