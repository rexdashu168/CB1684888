#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可轉債Excel資料解析腳本
用於解析元大證券提供的Excel檔案，轉換成JSON格式
"""

import pandas as pd
import json
import sys
from datetime import datetime

def parse_quote_sheet(excel_file):
    """解析報價單工作表"""
    df = pd.read_excel(excel_file, sheet_name='報價單', skiprows=4)
    df = df.dropna(subset=[df.columns[0]])
    
    # 建立資料結構 (需要根據實際欄位調整)
    quotes = []
    for idx, row in df.iterrows():
        try:
            quote = {
                "name": str(row.iloc[0]) if pd.notna(row.iloc[0]) else "",
                "code": str(row.iloc[1]) if pd.notna(row.iloc[1]) else "",
                "tcri": str(row.iloc[2]) if pd.notna(row.iloc[2]) else "",
                # 根據實際欄位繼續添加
            }
            if quote["code"]:  # 確保有代碼
                quotes.append(quote)
        except Exception as e:
            continue
    
    return quotes

def parse_basic_data(excel_file):
    """解析基本資料檔工作表"""
    df = pd.read_excel(excel_file, sheet_name='基本資料檔', skiprows=3)
    df = df.dropna(subset=[df.columns[0]])
    
    basic_data = []
    for idx, row in df.iterrows():
        try:
            data = {
                "code": str(row.iloc[0]) if pd.notna(row.iloc[0]) else "",
                "name": str(row.iloc[1]) if pd.notna(row.iloc[1]) else "",
                # 根據實際欄位繼續添加
            }
            if data["code"] and data["code"] != "代號":
                basic_data.append(data)
        except Exception as e:
            continue
    
    return basic_data

def parse_daily_quotes(excel_file):
    """解析CB每日行情表"""
    df = pd.read_excel(excel_file, sheet_name='CB每日行情表20251023', skiprows=1)
    df = df.dropna(subset=[df.columns[0]])
    
    daily_quotes = []
    for idx, row in df.iterrows():
        try:
            quote = {
                "code": str(row['代碼']) if pd.notna(row.get('代碼')) else "",
                "name": str(row['名稱  ']).strip() if pd.notna(row.get('名稱  ')) else "",
                "industry": str(row['產業']) if pd.notna(row.get('產業')) else "",
                "cb_close": float(row['CB收盤價']) if pd.notna(row.get('CB收盤價')) else 0,
                "volume": int(row['成交量']) if pd.notna(row.get('成交量')) else 0,
                "stock_price": float(row['股價']) if pd.notna(row.get('股價')) else 0,
                "conversion_price": float(row['轉換價格']) if pd.notna(row.get('轉換價格')) else 0,
                "conversion_value": float(row['轉換價值']) if pd.notna(row.get('轉換價值')) else 0,
                "premium_discount": float(row['溢(折)價%']) if pd.notna(row.get('溢(折)價%')) else 0,
            }
            if quote["code"]:
                daily_quotes.append(quote)
        except Exception as e:
            continue
    
    return daily_quotes

def parse_outstanding(excel_file):
    """解析流通在外餘額"""
    df = pd.read_excel(excel_file, sheet_name='CB流通在外餘額20251023', skiprows=1)
    df = df.dropna(subset=[df.columns[0]])
    
    outstanding = []
    for idx, row in df.iterrows():
        try:
            if idx == 0:  # 跳過標題行
                continue
            data = {
                "code": str(int(row.iloc[0])) if pd.notna(row.iloc[0]) else "",
                "name": str(row.iloc[1]) if pd.notna(row.iloc[1]) else "",
                "this_week": int(row.iloc[2]) if pd.notna(row.iloc[2]) else 0,
                # 根據實際欄位繼續添加
            }
            if data["code"]:
                outstanding.append(data)
        except Exception as e:
            continue
    
    return outstanding

def parse_excel_to_json(excel_file, output_dir):
    """
    解析完整的Excel檔案並輸出JSON
    
    參數:
        excel_file: str - Excel檔案路徑
        output_dir: str - 輸出目錄
    """
    print(f"正在解析: {excel_file}")
    
    # 取得日期 (從檔名)
    date_str = excel_file.split('元大證選擇權')[-1].replace('.xlsx', '')
    
    try:
        # 解析各工作表
        result = {
            "date": date_str,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "quotes": parse_quote_sheet(excel_file),
            "basic_data": parse_basic_data(excel_file),
            "daily_quotes": parse_daily_quotes(excel_file),
            "outstanding": parse_outstanding(excel_file),
        }
        
        # 儲存JSON
        output_file = f"{output_dir}/cb_data_{date_str}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 解析完成!")
        print(f"   日期: {date_str}")
        print(f"   報價單: {len(result['quotes'])}筆")
        print(f"   基本資料: {len(result['basic_data'])}筆")
        print(f"   每日行情: {len(result['daily_quotes'])}筆")
        print(f"   流通餘額: {len(result['outstanding'])}筆")
        print(f"   輸出檔案: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 解析失敗: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方式: python3 excel_parser.py <Excel檔案路徑>")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    output_dir = "data/static"
    
    parse_excel_to_json(excel_file, output_dir)
