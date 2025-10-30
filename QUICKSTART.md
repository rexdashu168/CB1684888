# 快速啟動指南 🚀

## 第一次使用 (本地測試)

### 1. 開啟網頁
直接用瀏覽器開啟 `web/index.html`

你會看到一個完整的可轉債查詢工具，包含：
- 📊 週報總覽
- 📈 成交量排行
- 📊 漲跌幅排行
- 🔄 轉換追蹤
- ⚠️ 贖回公告
- 📉 趨勢分析(需累積資料)

### 2. 測試資料解析

```bash
# 解析Excel檔案
python3 scripts/excel_parser.py /path/to/元大證選擇權20251027.xlsx

# 生成週報範本
python3 scripts/pdf_parser.py template
```

## 部署到GitHub (正式使用)

### 快速部署三步驟

```bash
# 1. 初始化並上傳到GitHub
git init
git add .
git commit -m "初始化可轉債查詢工具"
git remote add origin https://github.com/你的用戶名/cb-tools.git
git push -u origin main

# 2. 啟用GitHub Pages
# 前往 Settings > Pages > Source 選擇 main 分支

# 3. 網站就完成了！
# 網址: https://你的用戶名.github.io/cb-tools/
```

## 每週更新流程

### 更新Excel資料 (每日)

```bash
# 1. 放置新的Excel檔案到專案資料夾
# 2. 解析
python3 scripts/excel_parser.py 元大證選擇權20251104.xlsx

# 3. 上傳
git add data/static/
git commit -m "更新CB資料 2025/11/04"
git push
```

### 新增週報資料 (每週)

```bash
# 1. 複製範本
cp data/weekly/template.json data/weekly/20251104-1108.json

# 2. 編輯檔案 (填入PDF週報的資料)
# 使用任何文字編輯器開啟並填入資料

# 3. 上傳
git add data/weekly/20251104-1108.json
git commit -m "新增週報 2025/11/04-11/08"
git push
```

## 資料填寫範例

### 週報JSON填寫範例

```json
{
  "week_period": "2025/11/04~2025/11/08",
  "date": "2025-11-08",
  "top_volume": [
    {
      "rank": 1,
      "code": "30454",
      "name": "台灣大四",
      "volume": 5000
    },
    // ... 繼續填入其他資料
  ],
  // ... 其他欄位
}
```

## 常見問題

### Q: 如何確認網頁正常運作？
A: 在瀏覽器中按F12開啟開發者工具，查看Console是否有錯誤訊息

### Q: 資料沒有顯示？
A: 檢查JSON檔案格式是否正確，可以使用線上JSON驗證工具

### Q: 如何自訂網頁樣式？
A: 編輯 `web/index.html` 中的CSS部分

### Q: 如何新增功能？
A: 修改 `web/index.html` 中的React組件

## 檔案結構說明

```
cb-tools/
├── web/
│   └── index.html          ← 網頁主程式（唯一需要的檔案）
├── data/
│   ├── static/             ← Excel解析後的資料（會覆蓋）
│   └── weekly/             ← 週報資料（會累積）
│       ├── template.json   ← 範本檔案
│       └── YYYYMMDD-YYYYMMDD.json
├── scripts/
│   ├── excel_parser.py     ← Excel解析工具
│   └── pdf_parser.py       ← PDF解析工具
├── README.md               ← 完整說明文件
├── DEPLOY.md               ← GitHub部署指南
└── QUICKSTART.md           ← 本檔案
```

## 下一步

1. ✅ 本地測試網頁功能
2. ✅ 準備第一週的資料
3. ✅ 部署到GitHub Pages
4. ✅ 測試線上版本
5. ✅ 開始每週更新資料

## 聯絡支援

如有任何問題，歡迎透過以下方式聯絡：
- 方格子部落格: Rex大叔
- GitHub Issues: 在專案頁面提出問題

---

**祝你使用愉快！** 🎉

希望這個工具能幫助你和投資朋友做出更好的決策。
