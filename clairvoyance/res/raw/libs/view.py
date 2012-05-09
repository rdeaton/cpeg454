from common import droid, path
import os

class View(object):
    def __init__(self, layout, file = True):
        """
        Takes the layout as either a string, or a filename to load from
        the layouts directory, according to how *file* is set.
        """
        
        if file:
            with open(os.path.join(path, file), 'r') as f:
                self.layout = f.read()
        else:
            self.layout = layout
        
    def on_enter(self):
        droid.fullShow(self.layout)
        
    def on_exit(self):
        pass
        
    