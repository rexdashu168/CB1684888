#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
週報Excel轉JSON工具
讓你用Excel填寫週報資料，自動轉換成JSON格式
"""

import pandas as pd
import json
import sys
from datetime import datetime

def excel_to_json(excel_file):
    """
    將週報Excel轉換成JSON格式
    
    參數:
        excel_file: Excel檔案路徑
    """
    
    print(f"📖 讀取Excel檔案: {excel_file}")
    
    try:
        # 讀取基本資訊
        df_info = pd.read_excel(excel_file, sheet_name='1.基本資訊')
        week_period = df_info.loc[df_info['項目'] == '週報期間', '內容'].values[0]
        date = df_info.loc[df_info['項目'] == '資料日期', '內容'].values[0]
        
        # 讀取成交量排行
        df_volume = pd.read_excel(excel_file, sheet_name='2.成交量排行')
        df_volume = df_volume[df_volume['代碼'].notna() & (df_volume['代碼'] != '')]
        top_volume = []
        for idx, row in df_volume.iterrows():
            top_volume.append({
                "rank": int(row['排名']),
                "code": str(int(row['代碼'])),
                "name": str(row['名稱']),
                "volume": int(row['成交量(張)'])
            })
        
        # 讀取漲幅排行
        df_gainers = pd.read_excel(excel_file, sheet_name='3.漲幅排行')
        df_gainers = df_gainers[df_gainers['代碼'].notna() & (df_gainers['代碼'] != '')]
        top_gainers = []
        for idx, row in df_gainers.iterrows():
            top_gainers.append({
                "rank": int(row['排名']),
                "code": str(int(row['代碼'])),
                "name": str(row['名稱']),
                "close_price": float(row['收盤價']),
                "change_pct": float(row['漲幅%'])
            })
        
        # 讀取跌幅排行
        df_losers = pd.read_excel(excel_file, sheet_name='4.跌幅排行')
        df_losers = df_losers[df_losers['代碼'].notna() & (df_losers['代碼'] != '')]
        top_losers = []
        for idx, row in df_losers.iterrows():
            top_losers.append({
                "rank": int(row['排名']),
                "code": str(int(row['代碼'])),
                "name": str(row['名稱']),
                "close_price": float(row['收盤價']),
                "change_pct": float(row['跌幅%'])
            })
        
        # 讀取轉換追蹤
        df_conversion = pd.read_excel(excel_file, sheet_name='5.轉換追蹤')
        df_conversion = df_conversion[df_conversion['代碼'].notna() & (df_conversion['代碼'] != '')]
        conversions = []
        for idx, row in df_conversion.iterrows():
            conversions.append({
                "code": str(int(row['代碼'])),
                "name": str(row['名稱']),
                "this_week": int(row['本週張數']),
                "last_week": int(row['上週張數']),
                "converted": int(row['轉換張數']),
                "remaining_pct": float(row['剩餘比率%'])
            })
        
        # 讀取贖回公告
        df_redemption = pd.read_excel(excel_file, sheet_name='6.贖回公告')
        df_redemption = df_redemption[df_redemption['代碼'].notna() & (df_redemption['代碼'] != '')]
        redemptions = []
        for idx, row in df_redemption.iterrows():
            redemptions.append({
                "code": str(int(row['代碼'])),
                "name": str(row['名稱']),
                "original": int(row['原發行張數']),
                "outstanding": int(row['流通在外']),
                "remaining_pct": float(row['剩餘比率%']),
                "delist_date": str(row['終止掛牌日'])
            })
        
        # 組合成完整的JSON
        weekly_data = {
            "week_period": str(week_period),
            "date": str(date),
            "top_volume": top_volume,
            "top_gainers": top_gainers,
            "top_losers": top_losers,
            "conversions": conversions,
            "redemptions": redemptions
        }
        
        # 產生檔案名稱
        # 從週報期間提取日期: 2025/10/20~2025/10/23 -> 20251020-1023
        dates = week_period.replace('/', '').split('~')
        filename = f"data/weekly/{dates[0]}-{dates[1][-4:]}.json"
        
        # 儲存JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(weekly_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 轉換成功!")
        print(f"   週報期間: {week_period}")
        print(f"   資料日期: {date}")
        print(f"   成交量排行: {len(top_volume)} 檔")
        print(f"   漲幅排行: {len(top_gainers)} 檔")
        print(f"   跌幅排行: {len(top_losers)} 檔")
        print(f"   轉換追蹤: {len(conversions)} 檔")
        print(f"   贖回公告: {len(redemptions)} 檔")
        print(f"\n📄 已儲存: {filename}")
        print(f"\n下一步:")
        print(f"   git add {filename}")
        print(f"   git commit -m \"新增週報 {week_period}\"")
        print(f"   git push")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 轉換失敗: {str(e)}")
        print(f"\n請檢查:")
        print(f"   1. Excel檔案格式是否正確")
        print(f"   2. 工作表名稱是否正確")
        print(f"   3. 資料是否完整填寫")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方式:")
        print("  python3 scripts/excel_to_json.py 週報資料輸入範本.xlsx")
        print("\n或使用完整路徑:")
        print("  python3 scripts/excel_to_json.py data/weekly/週報資料輸入範本.xlsx")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    excel_to_json(excel_file)
