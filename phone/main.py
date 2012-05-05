import sys

if __name__ in ('__main__', '__android__'):
    import sl4a
    if len(sys.argv) == 3:
        addr = sys.argv[1], int(sys.argv[2])
    else:
        addr = '127.0.0.1', 8081
    droid = sl4a.Android(addr)
    if droid is None:
        print 'Failed to connect to SL4A server'

    for network in droid.wifiGetScanResults().result:
        print network