import time
import os
import sys
import zipfile

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    # We need to unpackage some things
    #support = zipfile.ZipFile(os.path.join(path, "support.zip"), 'r')
    #support.extractall(path)

    # Add the librares to our path
    sys.path.insert(0, path + '/libs')
    # fix_json casts all the unicode strings to ascii, for convenience
    import fix_json
    # On non-android systems, sl4a is the android module
    try:
        import android as sl4a
    except ImportError:
        import sl4a

    # In common we store a number of things shared throughout the program
    import common
    # On non-android systems, we allow a host and port to be passed for where
    # to connect to the RPC server
    if len(sys.argv) == 3:
        addr = sys.argv[1], sys.argv[2]
        droid = sl4a.Android(addr)
    else:
        droid = sl4a.Android()
    common.droid = droid
    common.path = path

    common.load_views()
    import manager


    # Turn on GPS at app startup
    #common.gps_lock()
    manager.push_view(common.views['startScreen'])
    #manager.push_view(common.views['settings'])
    manager.main_loop()
