#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可轉債週報資料解析腳本
用於解析元大證券提供的週報PDF，轉換成JSON格式
"""

import json
import re
from datetime import datetime
import sys

def parse_weekly_report(pdf_data):
    """
    解析週報資料
    
    參數:
        pdf_data: dict - 手動從PDF提取的資料
        
    返回:
        dict - 標準化的JSON資料
    """
    
    weekly_json = {
        "week_period": pdf_data.get("week_period", ""),
        "date": pdf_data.get("date", ""),
        "top_volume": pdf_data.get("top_volume", []),
        "top_gainers": pdf_data.get("top_gainers", []),
        "top_losers": pdf_data.get("top_losers", []),
        "conversions": pdf_data.get("conversions", []),
        "new_listings": pdf_data.get("new_listings", []),
        "redemptions": pdf_data.get("redemptions", []),
        "putbacks": pdf_data.get("putbacks", []),
        "maturities": pdf_data.get("maturities", [])
    }
    
    return weekly_json

def save_weekly_data(data, output_file):
    """
    儲存週報資料
    
    參數:
        data: dict - 週報資料
        output_file: str - 輸出檔案路徑
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 週報資料已儲存: {output_file}")
    print(f"   期間: {data['week_period']}")
    print(f"   成交量排行: {len(data['top_volume'])}檔")
    print(f"   漲幅排行: {len(data['top_gainers'])}檔")
    print(f"   跌幅排行: {len(data['top_losers'])}檔")
    print(f"   轉換追蹤: {len(data['conversions'])}檔")

def generate_weekly_template():
    """
    生成週報資料範本
    """
    template = {
        "week_period": "2025/MM/DD~2025/MM/DD",
        "date": "2025-MM-DD",
        "top_volume": [
            {"rank": 1, "code": "", "name": "", "volume": 0}
        ],
        "top_gainers": [
            {"rank": 1, "code": "", "name": "", "close_price": 0, "change_pct": 0}
        ],
        "top_losers": [
            {"rank": 1, "code": "", "name": "", "close_price": 0, "change_pct": 0}
        ],
        "conversions": [
            {"code": "", "name": "", "this_week": 0, "last_week": 0, "converted": 0, "remaining_pct": 0}
        ],
        "new_listings": [
            {"code": "", "name": "", "method": "競拍/詢圈", "amount": 0, "conversion_price": 0, "listing_date": ""}
        ],
        "redemptions": [
            {"code": "", "name": "", "original": 0, "outstanding": 0, "remaining_pct": 0, "delist_date": ""}
        ],
        "putbacks": [
            {"code": "", "name": "", "putback_date": "", "original": 0, "outstanding": 0, "remaining_pct": 0}
        ],
        "maturities": [
            {"code": "", "name": "", "maturity_date": "", "original": 0, "outstanding": 0, "stop_conversion_start": "", "stop_conversion_end": "", "remaining_pct": 0}
        ]
    }
    
    return template

if __name__ == "__main__":
    # 使用範例
    print("可轉債週報資料解析腳本")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "template":
        # 生成範本
        template = generate_weekly_template()
        output_file = "data/weekly/template.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        print(f"✅ 範本已生成: {output_file}")
    else:
        print("使用方式:")
        print("  python3 pdf_parser.py template  - 生成資料範本")
        print("\n請根據PDF內容手動填寫資料到JSON檔案中")
