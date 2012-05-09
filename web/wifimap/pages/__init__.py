"""
This module controls dynamic content of the web application. Each submodule
contains functions decorated with app.route and app.allow to allow the framework
to dispatch requests to each function.
"""


import os
dir = os.listdir(os.path.dirname(__file__))
for d in dir:
    if d[-3:] == '.py' and d[0] != '_' and d[0] != '.':
        __import__("wifimap.pages." + d[:-3], fromlist = ["*"])
