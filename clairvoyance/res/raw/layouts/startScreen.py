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
    layout = open(os.path.join(common.path, 'layouts', 'startScreen.xml'), 'r').read()
    droid.fullShow(layout)
    
    prefs = droid.prefGetValue('settings', 'clairvoyance').result
    if prefs is not None:
        settings = json.loads(prefs)
    droid.clearOptionsMenu()
    droid.addOptionsMenuItem("Close Application","EXIT_APP",None,"star_on")
    


def close_view():
    droid.fullDismiss()


def handle_event(event):
    """
    This should handle events one at a time. It should return a manager.EVENT_*
    constant.
    """
    if event["name"]=="click":
        id = event["data"]["id"]
        if id == "collectData":
            pass
        elif id == "viewMaps":
            pass
        elif id == "changeSettings":
            manager.push_view(common.views['settings'])
        elif id == "viewAbout":
            manager.push_view(common.views['about'])
            
    elif event["name"]=="screen":
        if event["data"]=="destroy":
            # manager.close_app()
            return manager.EVENT_CONSUME
    elif event["name"] == "EXIT_APP":
        manager.close_app()
    
    
    return manager.EVENT_UNUSED