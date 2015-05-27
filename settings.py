#!/usr/bin/python
#-*- coding: UTF-8 -*-
# 設定MARC格式須包含哪些欄位段落。
#comsection = ('000', '001', '010', '200', '210', '205', '101', '700', '805')
comsection = ('000', '001', '200')
# 設定MARC資料輸出路徑。
outputpath = ('./out.marc')
isostep = 12

# 設定MARC識別字符
endofrec = '\x1d'
sepsign = '\x1e'
dollarsign = '\x1f'

# Set convert decode & encode
fencode = 'big5'
tencode = 'utf8'
