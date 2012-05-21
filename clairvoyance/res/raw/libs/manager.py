from common import droid

# Pass this along to the next handler unused
EVENT_UNUSED  = 0
# Do not pass this along to the next handler at all
EVENT_CONSUME = 1
# Note this event was used, but still pass it along for others
EVENT_USED    = 2

event_handlers = []
views = []

def add_event_handler(handler):
    event_handlers.append(handler)
    
def remove_event_handler(handler):
    try:
        event_handlers.remove(handler)
    except Exception:
        pass

def push_view(view):
    if len(views) > 0:
        views[-1].close_view()
        event_handlers.remove(views[-1].handle_event)
    views.append(view)
    event_handlers.append(view.handle_event)
    view.open_view()
    
def pop_view():
    views[-1].close_view()
    event_handlers.remove(views[-1].handle_event)
    views.pop()
    if len(views) == 0:
        exit()

def swap_view(view):
    if len(views) == 0:
        push_view(view)
    else:
        views[-1].close_view()
        event_handlers.remove(views[-1].handle_event)
        views.pop()
        views.append(view)
        view.open_view()
        event_handlers.append(view.handle_event)

def main_loop():
    while True:
        event = droid.eventWait().result
        used = False
        for handler in event_handlers:
            r = handler(event)
            if EVENT_CONSUME:
                continue
            if EVENT_USED:
                used = True
        if used is False:
            print 'UNUSED EVENT: ' + str(event)
            
def close_app():
    views[-1].close_view()
    exit()
