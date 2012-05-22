import manager
import common
import os
import json
from common import droid


def open_view():
  
    layout = open(os.path.join(common.path, 'layouts', 'startScreen.xml'), 'r').read()
    droid.fullShow(layout)
    droid.fullSetProperty("mainLogo", "src", 'file:///' + os.path.join(common.path, 'layouts', 'image.png'))
    
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
            manager.push_view(common.views['collectData'])
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