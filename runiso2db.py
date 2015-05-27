#!/usr/local/bin/python
#-*- coding: UTF-8 -*-

import flybase
import settings
from creader import Reader
import sys
from fieldmap import *
from flybase import webdata

filepath = sys.argv[1]

db = flybase.fbopen('./catalog', 'c')
#db = flybase.fbopen('../db/catalog', 'c')

def getValue(obj, rules):
    result = ''
    for x in rules:
        k = x.keys()[0]
        v = x.values()[0]
        if not result:
            if k and v:
                result = obj.GetFieldData(k,v)
            elif not v:
                result = obj.GetFieldData(k)
            else:
                result = ''
    if result and '"' in result:
        result = result.replace('"', ' ')
    return result

def main():
    count = int(webdata.nextpmkey(db, '###########'))
    isos = open(filepath).read().split('\x1d')
    ib = mti = mau = pyr = pub = plc = ver = msb = lg = id2 = aun = cl = ppg = gram = cu = omarc = ''
    for iso in isos:
        marc = Reader(iso)
        if marc.OutMARC():
            rid = str(count)
            ib = getValue(marc, field['ib'])
            mti = getValue(marc, field['mti'])
            mau = getValue(marc, field['mau'])
            pyr = getValue(marc, field['pyr'])
            pub = getValue(marc, field['pub'])
            plc = getValue(marc, field['plc'])
            ver = getValue(marc, field['ver'])
            msb = getValue(marc, field['msb'])
            lg = getValue(marc, field['lg'])
            id2 = getValue(marc, field['id2'])
            aun = getValue(marc, field['aun'])
            cl = getValue(marc, field['cl'])
            ppg = getValue(marc, field['ppg'])
            gram = getValue(marc, field['gram'])
            loc = getValue(marc, field['loc']).upper()
            try:
                loc = location[loc]
            except KeyError:
                pass

            if ib:
                # 判斷isbn是否在在資料庫，若是則更新該筆書目館藏地、作者號、分類號及書目紀錄號資訊。
                if len(db.select('ib', ib)):
                    for x in list(db.select('ib', ib)):
                        loclist = db[x, 'loc']
                        aunlist = db[x, 'aun']
                        cllist = db[x, 'cl']
                        id2list = db[x, 'id2']
                        if not loclist.count(loc):
                            loclist.append(loc)
                            aunlist.append(aun)
                            cllist.append(cl)
                            id2list.append(id2)
                            db.lock()
                            db[x, 'loc'] = loclist
                            db[x, 'aun'] = aunlist
                            db[x, 'cl'] = cllist
                            db[x, 'id2'] = id2list
                            db.unlock()
                        else:
                            pass

                else:
                    D = {'id': rid, 'ib':[ib], 'mti':[mti], 'mau':[mau], 'pyr':[pyr], 'pub':[pub], 'cu':[cu], 'plc':[plc], 'ver':[ver], 'msb':[msb], 'lg':[lg], 'id2':[id2], 'aun':[aun], 'cl':[cl], 'ppg':[ppg], 'gram':[gram], 'marc':[omarc], 'loc':[loc]}
                    count = count + 1
                    db.lock()
                    db.new(D)
                    db.unlock()
            elif mti and mau and pyr and pub:
                # 當該筆資料沒有isbn時，用mti mau pyr pub判斷資料庫是否有此資料。
                r = list(db.query('mti="%s" and mau="%s" and pyr="%s" and pub="%s"' % (mti, mau, pyr, pub)))
                if len(r):
                    for x in r:
                        loclist = db[x, 'loc']
                        aunlist = db[x, 'aun']
                        cllist = db[x, 'cl']
                        id2list = db[x, 'id2']
                        if not loclist.count(loc):
                            loclist.append(loc)
                            aunlist.append(aun)
                            cllist.append(cl)
                            id2list.append(id2)
                            db.lock()
                            db[x, 'loc'] = loclist
                            db[x, 'aun'] = aunlist
                            db[x, 'cl'] = cllist
                            db[x, 'id2'] = id2list
                            db.unlock()
                        else:
                            pass
                else:
                    D = {'id': rid, 'ib':[ib], 'mti':[mti], 'mau':[mau], 'pyr':[pyr], 'pub':[pub], 'plc':[plc], 'ver':[ver], 'msb':[msb], 'lg':[lg], 'id2':[id2], 'aun':[aun], 'cl':[cl], 'ppg':[ppg], 'gram':[gram], 'loc':[loc]}
                    count = count + 1
                    db.lock()
                    db.new(D)
                    db.unlock()
            else:
                pass

if __name__ == '__main__':
    main()
