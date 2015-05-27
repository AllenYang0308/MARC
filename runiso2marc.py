#!/usr/bin/python
#-*- coding: UTF-8 -*-

from iso2marc import *
import sys

filepath = sys.argv[1]
func = sys.argv[2]
err =0

def main():
    err = 0
    try:
        d = open(filepath)
    except:
        print "Error -- No such file or directory."
        sys.exit(1)

    alliso = d.read().split('\x1d')

    #for x in alliso[:10]:
    for x in alliso:
        marc = MARC()
        marc.SetEncode('big5', 'utf8')
        marc.GetHeader(x)
        marc.GetData(x)
        if marc.CheckMARC(marc.OutHeaderList(), marc.OutDataRow()):
            marc.PrintMARC(func)
            #pass
        else:
            #print x
            err = err + 1
    print 'Error Count: %s' % (err)

if __name__ == '__main__':
    main()
