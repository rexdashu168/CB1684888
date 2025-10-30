# GitHub部署指南

## 步驟一：建立GitHub Repository

1. 登入GitHub帳號
2. 點選右上角的 "+" → "New repository"
3. 填寫資訊：
   - Repository name: `cb-tools` (或自訂名稱)
   - Description: 可轉債查詢工具 - Rex大叔投資資料庫
   - 選擇 Public (公開) 或 Private (私有)
   - 不勾選 "Initialize with README" (我們已有README)
4. 點選 "Create repository"

## 步驟二：上傳專案到GitHub

```bash
# 1. 初始化Git (在專案資料夾中)
cd cb-tools
git init

# 2. 添加所有檔案
git add .

# 3. 第一次提交
git commit -m "初始化可轉債查詢工具"

# 4. 連結到GitHub (替換成你的GitHub用戶名和倉庫名)
git remote add origin https://github.com/你的用戶名/cb-tools.git

# 5. 推送到GitHub
git branch -M main
git push -u origin main
```

## 步驟三：啟用GitHub Pages

1. 進入你的Repository頁面
2. 點選 "Settings" (設定)
3. 左側選單找到 "Pages"
4. 在 "Source" 下拉選單中選擇 "main" 分支
5. 資料夾選擇 "/web" (或 root，如果網頁在根目錄)
6. 點選 "Save"
7. 等待幾分鐘，網站就會部署好

網站網址會是：`https://你的用戶名.github.io/cb-tools/`

## 步驟四：修改網頁中的資料讀取路徑

編輯 `web/index.html`，將資料讀取路徑改為GitHub的raw檔案連結：

```javascript
// 原本的本地路徑
const dataPath = '../data/weekly/20251020-1023.json';

// 改為GitHub raw路徑
const dataPath = 'https://raw.githubusercontent.com/你的用戶名/cb-tools/main/data/weekly/20251020-1023.json';
```

## 步驟五：每次更新資料

### 更新靜態資料 (Excel)

```bash
# 1. 解析新的Excel檔案
python3 scripts/excel_parser.py 元大證選擇權20251027.xlsx

# 2. 提交更新
git add data/static/
git commit -m "更新CB資料 2025/10/27"
git push

# 網頁會自動讀取最新資料
```

### 新增週報資料

```bash
# 1. 建立新週報檔案
cp data/weekly/template.json data/weekly/20251027-1030.json

# 2. 編輯檔案，填入資料
nano data/weekly/20251027-1030.json

# 3. 提交更新
git add data/weekly/20251027-1030.json
git commit -m "新增週報 2025/10/27-10/30"
git push

# 網頁會自動累積顯示
```

## 快速指令備忘

```bash
# 查看狀態
git status

# 查看變更
git diff

# 添加所有變更
git add .

# 提交
git commit -m "說明訊息"

# 推送到GitHub
git push

# 拉取最新版本
git pull

# 查看歷史記錄
git log --oneline
```

## 進階設定：自動化更新

### 使用GitHub Actions自動解析Excel

建立 `.github/workflows/update-data.yml`:

```yaml
name: Update CB Data

on:
  push:
    paths:
      - '**.xlsx'

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          pip install pandas openpyxl
      
      - name: Parse Excel files
        run: |
          for file in *.xlsx; do
            python3 scripts/excel_parser.py "$file"
          done
      
      - name: Commit results
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/
          git commit -m "自動更新資料" || exit 0
          git push
```

這樣當你上傳Excel檔案時，GitHub會自動執行解析並更新JSON資料。

## 疑難排解

### 問題：網頁無法讀取資料

**解決方式**：
1. 確認資料檔案路徑正確
2. 使用瀏覽器開發者工具(F12)查看錯誤訊息
3. 確認GitHub Pages已啟用並部署成功

### 問題：CORS錯誤

**解決方式**：
使用GitHub的raw內容連結，或設定CORS header

### 問題：資料未更新

**解決方式**：
1. 清除瀏覽器快取
2. 確認git push成功
3. 等待GitHub Pages重新部署(約1-5分鐘)

## 相關連結

- GitHub Pages說明: https://pages.github.com/
- Git基本教學: https://git-scm.com/book/zh-tw/v2
- GitHub Actions文件: https://docs.github.com/en/actions
