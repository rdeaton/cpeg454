import manager
import common
import os
import json
from common import droid

settings = {
     'scan_interval' : 60,
     'throughput_interval' : 60,
     'minimum_battery' : 15}



def open_view():
    global settings
    layout = open(os.path.join(common.path, 'layouts', 'about.xml'), 'r').read()
    droid.fullShow(layout)

    #set the text fields
    droid.fullSetProperty("Title", "text", "Help/About")
    droid.fullSetProperty("DevsTitle", "text", "Developers")
    droid.fullSetProperty("devNames", "text", "Robert Deaton - rdeaton@udel.edu\nGraeme Lawes - gclawes@udel.edu\nEric McGinnis - ericmcg@udel.edu")
    droid.fullSetProperty("infoTitle", "text", "Purpose")
    droid.fullSetProperty("info", "text", "The purpose of this application is to help the University of Delaware's network administrations " +
                                           "easily develop coverage maps of the UD's wireless infrastructure.  The application will provide " +
                                           "data relating to the signal strength and throughput of the network at corresponding GPS locations " +
                                           "This data will be used to construct a heatmap that will allow administrators to see which areas " +
                                           "suffer from poor signal strength and/or network congestion.")
    
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
