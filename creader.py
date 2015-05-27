#!/usr/local/bin/python
#-*- coding: UtF-8 -*-

from iso2marc import MARC
import settings
import sys

class Reader(MARC):
    '''
    繼承MARC類別，在產生Reader實體時必須先引入iso資料，產生實體時會自動處理iso檔轉為MARC格式。
    '''
    def __init__(self, iso):
        super(Reader, self).__init__()
        self.__dollarsign = settings.dollarsign
        self.__sepsign = settings.sepsign
        self.__endofrec = settings.endofrec
        self.SetEncode(settings.fencode, settings.tencode)
        self.GetHeader(iso)
        self.GetData(iso)

    def GetDataSection(self, field):
        marc = self.OutMARC()
        try:
            idxs = marc[field].index(self.__dollarsign)
            strdata = marc[field][idxs:].split(' ')[0].rstrip()
        except:
            strdata = marc[field].split(' ')[0].strip()
        return strdata

    def GetFieldData(self, field, sub=None):

        subfield = []
        subdatas = []
        self.PrintMARC()
        if field not in self.OutHeaderList():
            return ''
        strdata = self.GetDataSection(field)
        if self.__dollarsign not in strdata:
            fielddata = strdata
        else:
            subfieldlist = strdata.split(self.__dollarsign)
            for x in subfieldlist:
                try:
                    subfield.append(x[0])
                    subdatas.append(x[1:])
                except:
                    pass
            r = dict(zip(subfield, subdatas))
            try:
                fielddata = r[sub]
            except:
                #fielddata = None
                fielddata = ''

        return fielddata

