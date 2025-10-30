#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動抓取CB價格腳本
每天從證交所抓取CB交易資訊並更新
"""

import requests
import json
import pandas as pd
from datetime import datetime
import time
import os

def fetch_twse_cb_data():
    """
    從台灣證交所抓取CB交易資料
    """
    print(f"🔍 開始抓取CB價格資料... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 證交所CB交易資訊API
    url = "https://www.twse.com.tw/exchangeReport/BWIBBU_d"
    
    params = {
        "response": "json",
        "date": datetime.now().strftime('%Y%m%d')
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                print(f"✅ 成功抓取 {len(data['data'])} 筆CB資料")
                return parse_twse_data(data)
            else:
                print("⚠️  今日無交易資料，使用上次資料")
                return None
        else:
            print(f"❌ HTTP錯誤: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        return None

def parse_twse_data(raw_data):
    """
    解析證交所回傳的資料
    """
    cb_list = []
    
    for item in raw_data['data']:
        try:
            # 證交所資料格式:
            # [代號, 名稱, 收盤價, 漲跌, 成交量, ...]
            
            cb_data = {
                "code": item[0].strip(),
                "name": item[1].strip(),
                "close_price": float(item[2].replace(',', '')) if item[2] != '--' else None,
                "change": float(item[3].replace(',', '')) if item[3] != '--' else 0,
                "change_percent": float(item[4].replace('%', '')) if item[4] != '--' else 0,
                "volume": int(item[5].replace(',', '')) if item[5] != '--' else 0,
                "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if cb_data["close_price"] is not None:
                cb_list.append(cb_data)
                
        except Exception as e:
            print(f"⚠️  解析錯誤 {item[0]}: {str(e)}")
            continue
    
    return cb_list

def fetch_tpex_cb_data():
    """
    從櫃買中心抓取CB資料（補充上櫃CB）
    """
    print("🔍 抓取櫃買中心CB資料...")
    
    url = "https://www.tpex.org.tw/web/bond/tradeinfo/bond_close_ajax.php"
    
    params = {
        "l": "zh-tw",
        "d": datetime.now().strftime('%Y/%m/%d')
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'aaData' in data:
                print(f"✅ 成功抓取 {len(data['aaData'])} 筆櫃買CB資料")
                return parse_tpex_data(data)
            else:
                return []
        else:
            return []
            
    except Exception as e:
        print(f"⚠️  櫃買中心抓取失敗: {str(e)}")
        return []

def parse_tpex_data(raw_data):
    """
    解析櫃買中心資料
    """
    cb_list = []
    
    for item in raw_data['aaData']:
        try:
            # 只抓可轉債（跳過其他債券）
            if '轉' not in item[1]:
                continue
                
            cb_data = {
                "code": item[0].strip(),
                "name": item[1].strip(),
                "close_price": float(item[2].replace(',', '')) if item[2] != '--' else None,
                "change": float(item[3].replace(',', '')) if item[3] != '--' else 0,
                "change_percent": float(item[4].replace('%', '')) if item[4] != '--' else 0,
                "volume": int(item[5].replace(',', '')) if item[5] != '--' else 0,
                "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if cb_data["close_price"] is not None:
                cb_list.append(cb_data)
                
        except Exception as e:
            continue
    
    return cb_list

def save_cb_prices(cb_data):
    """
    儲存CB價格資料
    """
    if not cb_data or len(cb_data) == 0:
        print("⚠️  無資料可儲存")
        return False
    
    # 建立資料夾
    os.makedirs('data/prices', exist_ok=True)
    
    # 儲存每日價格
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f"data/prices/cb_prices_{date_str}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cb_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已儲存到: {filename}")
    
    # 同時更新最新價格檔（供網頁使用）
    latest_file = "data/prices/latest.json"
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump({
            "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "date": date_str,
            "count": len(cb_data),
            "data": cb_data
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已更新最新價格檔: {latest_file}")
    
    return True

def main():
    """
    主程式
    """
    print("="*60)
    print("CB價格自動抓取程式")
    print("="*60)
    
    # 1. 抓取證交所資料
    twse_data = fetch_twse_cb_data()
    time.sleep(3)  # 禮貌性延遲
    
    # 2. 抓取櫃買中心資料
    tpex_data = fetch_tpex_cb_data()
    
    # 3. 合併資料
    all_data = []
    if twse_data:
        all_data.extend(twse_data)
    if tpex_data:
        all_data.extend(tpex_data)
    
    # 4. 儲存資料
    if len(all_data) > 0:
        save_cb_prices(all_data)
        print(f"\n✅ 完成！共抓取 {len(all_data)} 筆CB價格")
    else:
        print("\n⚠️  今日無交易資料")
    
    print("="*60)

if __name__ == "__main__":
    main()
