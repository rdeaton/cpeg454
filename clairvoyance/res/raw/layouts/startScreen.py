import manager
import common
import os
import json
from common import droid





def open_view():
  
    layout = open(os.path.join(common.path, 'layouts', 'startScreen.xml'), 'r').read()
    droid.fullShow(layout)
    droid.fullSetProperty("collectIcon", "src", 'file:///' + os.path.join(common.path, 'layouts', 'icons', 'collectIcon.png'))
    droid.fullSetProperty("settingsIcon", "src", 'file:///' + os.path.join(common.path, 'layouts', 'icons', 'settingsIcon.png'))
    droid.fullSetProperty("mapIcon", "src", 'file:///' + os.path.join(common.path,  'layouts', 'icons', 'mapIcon.png'))
    droid.fullSetProperty("aboutIcon", "src", 'file:///' + os.path.join(common.path, 'layouts', 'icons',  'aboutIcon.png'))
    
    prefs = droid.prefGetValue('settings', 'clairvoyance').result
    if prefs is not None:
        settings = json.loads(prefs)
    droid.clearOptionsMenu()
    droid.addOptionsMenuItem("Close Application","EXIT_APP",None,"ic_menu_close_clear_cancel")
    


def close_view():
    droid.fullDismiss()


def handle_event(event):
    """
    This should handle events one at a time. It should return a manager.EVENT_*
    constant.
    """
    if event["name"]=="click":
        id = event["data"]["id"]
        if id == "collectIcon":
            manager.push_view(common.views['collectData'])
        elif id == "mapIcon":
            droid.view("http://107.20.202.68:5052/static/launch.html")
        elif id == "settingsIcon":
            manager.push_view(common.views['settings'])
        elif id == "aboutIcon":
            manager.push_view(common.views['about'])
            
    elif event["name"]=="screen":
        if event["data"]=="destroy":
            # manager.close_app()
            return manager.EVENT_CONSUME
    elif event["name"] == "EXIT_APP":
        droid.stopLocating()
        manager.close_app()
    else:
        print "Unused event in startScreen."
        return manager.EVENT_UNUSED