import sys

if __name__ in ('__main__', '__android__'):
    import sl4a
    if len(sys.argv) == 3:
        addr = sys.argv[1], int(sys.argv[2])
    droid = sl4a.Android(addr)
    
    # Start inserting code here
