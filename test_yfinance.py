#!/usr/bin/env python3
"""测试yfinance功能"""

import yfinance as yf

print("测试yfinance库...")
try:
    # 测试获取单个ETF数据
    ticker = yf.Ticker("KWEB")
    data = ticker.history(period="2d")
    print(f"KWEB数据: {data}")
    
    # 计算涨跌幅
    if len(data) >= 2:
        pct = (data["Close"].iloc[-1] / data["Close"].iloc[-2] - 1) * 100
        print(f"涨跌幅: {pct:.2f}%")
    else:
        print("数据不足")
except Exception as e:
    print(f"错误: {e}")
