這是一個提供書目資料ISO轉MARC格式的類別及實作，此類別提供幾種實作方式:

1. 取得標頭段(資料描述段) -- GetHeader及OutHeaderList
    GetHeader的操作方法，須引入單一ISO資料段，程式會自動提取出
    資料描述段進行處理，處理後的結果會儲存在物作成員headerlist
    中，使用者可以直接對headerlist進行操作，或使用OutHeaderList
    方法進行操作。
    MARC.GetHeader(data)
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
