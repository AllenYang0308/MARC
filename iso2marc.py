#!/usr/bin/python
#-*- coding: UTF-8 -*-

import settings

def outputfile(filepath, data):
    wf = open(filepath, 'a')
    print >> wf, data
    wf.close()

class MARC(object):
    def __doc__(self):
        """
            這是一個提供ISO轉MARC格式的類別及實作，此類別提供幾種實作方式
            1. 取得標頭段(資料描述段) -- GetHeader及OutHeaderList
                GetHeader的操作方法，須引入單一ISO資料段及長度位元數，程式
                會自動提取出資料描述段進行處理，處理後的結果會儲存在物作成
                員headerlist中，使用者可以直接對headerlist進行操作，或使用
                OutHeaderList方法進行操作。
                MARC.GetHeader(data, step)
                MARC.OutHeaderList()

            2. 取得資料 -- GetData及OutDataRow
                GetData的操作方法，須引入單一ISO資料段，程式會自動提取出資料
                段進行處理，並將處理結果儲存於物件成員datarowlist的陣列中。
                使用者可以直接對該成員進行操作或使用OutDataRow方法操作。
                MARC.GetData(data)
                MARC.OutDataRow()

            3. 列印MARC資料 -- PrintMARC
                使用者可以直接使用PrintMARC方法列印MARC資料，使用時須引入兩陣
                列資，MARC段落編號及MARC資料陣列，程式會自動將兩資料陣列結合成
                一字典型式資料再進行排序列印。
                MARC.PrintMARC([list key], [list data])
                可以直接使用MARC.OutHeaderList()產生key，由MARC.OutDataRow()產
                生資料代入PrintMARC方法列印。

            4. 檢查產生的MARC資料 -- CheckMARC
                使用CheckMARC時須引入ISO欄位及ISO資料，程式會利用設定檔案
                settings.comsection設定的參數進行ISO資料欄位判斷。
        """

    def __init__(self):
        """
        物件產生時會同時設定物件內部參數，
        sepsign: iso檔資料中用來分各資料段符號。
        dollarsign: 機讀格式中分爛中的錢字符號。
        datarowlist: 由iso讀出的資料段落。
        headerlist: 由iso讀出的欄位段落。
        fencode: 用來decode的編碼。
        tencode: 用來encode的編碼。
        """
        self.__endofrec = settings.endofrec
        self.__sepsign = settings.sepsign
        self.__dollarsign = settings.dollarsign
        self.__fencode = 'utf8'
        self.__tencode = 'utf8'
        self.headerlist = []
        self.datarowlist = []

    def SetEncode(self, fencode, tencode):
        if fencode == tencode:
            pass
        else:
            self.__fencode = fencode
            self.__tencode = tencode

    def GetHeader(self, data):
        header = data.split(self.__sepsign)[0]

        zerorowdata = '0' * settings.isostep
        startf = 0
        endf = stepf = int(settings.isostep)

        self.header = '%s%s' % (zerorowdata, header[24:])
        while self.header[startf:endf]:
            self.headerlist.append(self.header[startf:endf][:3])
            startf = startf + stepf
            endf = endf + stepf
        startf = 0
        endf = settings.isostep

    def OutHeaderList(self):
        return self.headerlist

    def GetData(self, data):
        try:
            marcdata = data.split(self.__sepsign)
            marcdata[0] = '%s %s' % (' ', marcdata[0][5:9])
            for i in marcdata:
                if '\x1f' in i:
                    datasection = '%s %s' % (i[0:2], i[2:])
                    self.datarowlist.append(datasection)
                else:
                    datasection = ' %s' % (i)
                    self.datarowlist.append(datasection)
        except:
            marcdata = []

    def OutDataRow(self):
        return self.datarowlist

    def CheckMARC(self, key, data):
        r = ''
        marcdata = dict(zip(key, data))
        if len(settings.comsection):
            r = [x for x in settings.comsection if x not in marcdata.keys()]
        if r:
            return 0
        else:
            return 1

    #def OutMARC(self, key, data):
    def OutMARC(self):
        if self.CheckMARC(self.headerlist, self.datarowlist):
            marcdata = dict(zip(self.headerlist, self.datarowlist))
        else:
            marcdata = None
        return marcdata

    #def PrintMARC(self, key, data, func=1):
    def PrintMARC(self, func=1):
        #marcdata = dict(zip(key, data))
        marcdata = self.OutMARC()
        filepath = settings.outputpath
        key = marcdata.keys()
        key.sort()

        for x in key:
            try:
                outmarc = '%s %s' % (x, marcdata[x].decode(self.__fencode).encode(self.__tencode))
            except:
                outmarc = '%s %s' % (x, marcdata[x])

            print outmarc
            if func == str(2):
                outputfile(filepath, outmarc)
        print self.__endofrec
        if func == str(2):
            outputfile(settings.outputpath, self.__endofrec)

