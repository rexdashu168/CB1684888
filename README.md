# 可轉債查詢工具 - Rex大叔投資資料庫

專業、即時、完整的CB市場資訊查詢平台

## 📋 功能特色

### 週報資料庫 (累積型資料)
- ✅ 成交量排行榜 - 追蹤市場熱門標的
- ✅ 漲跌幅排行榜 - 掌握價格波動
- ✅ 轉換追蹤 - 監控CB轉股動態
- ✅ 近期掛牌CB - 新發行標的資訊
- ✅ 贖回公告 - 公司執行贖回權追蹤
- ✅ 賣回資訊 - 投資人賣回權日期
- ✅ 到期資訊 - CB到期日管理

### 靜態資料查詢 (每次更新)
- 📊 報價單 - 最新CB報價資訊
- 📈 基本資料 - 完整的CB基本面資料
- 🔍 每日行情 - CB交易行情即時查詢
- 📉 流通餘額 - 各檔CB流通在外狀況
- ⚠️ 停止轉換資訊 - 停止轉換期間公告
- 💰 轉換價格調整 - 價格調整歷史記錄

### 趨勢分析 (累積資料後啟用)
- 📊 成交量趨勢圖
- 📈 價格走勢分析
- 🔄 轉換張數變化
- 🔥 市場熱門CB追蹤

## 📁 專案結構

```
cb-tools/
├── data/
│   ├── static/              # 靜態資料 (每次覆蓋更新)
│   │   └── cb_data_YYYYMMDD.json
│   └── weekly/              # 週報資料 (累積保存)
│       ├── 20251020-1023.json
│       ├── 20251027-1030.json
│       └── ...
├── scripts/
│   ├── excel_parser.py      # Excel解析腳本
│   └── pdf_parser.py        # PDF週報解析腳本
├── web/
│   └── index.html           # 網頁主程式
└── README.md
```

## 🚀 使用方式

### 1. 上傳Excel資料 (靜態資料)

將元大證券提供的Excel檔案上傳到GitHub:

```bash
# 解析Excel檔案
python3 scripts/excel_parser.py 元大證選擇權20251027.xlsx

# 上傳到GitHub
git add data/static/cb_data_20251027.json
git commit -m "更新CB資料 2025/10/27"
git push
```

### 2. 上傳週報資料 (累積型資料)

每週手動建立週報JSON檔案:

```bash
# 使用範本建立新週報
cp data/weekly/template.json data/weekly/20251027-1030.json

# 編輯檔案，填入本週資料
# (從PDF週報中提取資料)

# 上傳到GitHub
git add data/weekly/20251027-1030.json
git commit -m "新增週報 2025/10/27-10/30"
git push
```

### 3. 網頁自動更新

當資料上傳到GitHub後，網頁會自動讀取最新資料並更新顯示。

## 📊 資料格式說明

### 週報資料格式 (weekly/YYYYMMDD-YYYYMMDD.json)

```json
{
  "week_period": "2025/10/20~2025/10/23",
  "date": "2025-10-23",
  "top_volume": [
    {
      "rank": 1,
      "code": "30454",
      "name": "台灣大四",
      "volume": 4645
    }
  ],
  "top_gainers": [
    {
      "rank": 1,
      "code": "33571",
      "name": "臺慶科一",
      "close_price": 149.00,
      "change_pct": 11.19
    }
  ],
  "top_losers": [...],
  "conversions": [...],
  "redemptions": [...],
  "putbacks": [...],
  "maturities": [...]
}
```

### 靜態資料格式 (static/cb_data_YYYYMMDD.json)

```json
{
  "date": "20251027",
  "update_time": "2025-10-27 14:30:00",
  "quotes": [...],
  "basic_data": [...],
  "daily_quotes": [...],
  "outstanding": [...]
}
```

## 🛠️ 技術架構

- **前端**: React + JavaScript
- **資料格式**: JSON
- **資料來源**: GitHub Repository
- **更新方式**: Git Push自動更新

## 📝 更新流程

### 每日更新 (靜態資料)
1. 下載元大證券最新Excel檔案
2. 使用excel_parser.py解析
3. 上傳到GitHub (覆蓋舊資料)

### 每週更新 (週報資料)
1. 下載元大證券週報PDF
2. 手動建立JSON檔案 (參考範本)
3. 上傳到GitHub (不覆蓋，累積保存)

## 🎯 未來功能規劃

- [ ] 自動解析PDF功能
- [ ] Excel自動上傳功能
- [ ] 更多圖表分析
- [ ] 個股詳細資料頁面
- [ ] 自訂追蹤清單
- [ ] 價格提醒功能
- [ ] 歷史資料匯出

## 📧 聯絡方式

如有任何問題或建議，歡迎聯繫：
- 部落格：方格子 Rex大叔
- 專業認證：CFP國際認證理財規劃顧問

## ⚠️ 免責聲明

本資料僅供參考使用，資訊內容將力求正確，惟進行投資決策時，請投資人依據個人專業判斷，本工具不作任何資訊及獲利保證。

---

**資料來源**: 元大證券債券部  
**更新頻率**: 每日/每週  
**維護者**: Rex大叔
