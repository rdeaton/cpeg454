"""
The web module contains code which is specific to the web frontend, but is not
otherwise categorized (such as pages, templates, static, etc.). Code contained
here is meant to be transparent and not directly imported, only imported by the
relevant web launchers.

See individual files for comments on their contents.
"""

import os
dir = os.listdir(os.path.dirname(__file__))
for d in dir:
    if d[-3:] == '.py' and d[0] != '_':
        __import__("wifimap.web." + d[:-3], fromlist = ["*"])
