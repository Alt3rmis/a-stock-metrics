#!/usr/bin/env python3
"""简单测试脚本"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

from astock_metrics.data.external import fetch_china_etf, get_china_etf

print("测试 fetch_china_etf 函数...")
try:
    result = fetch_china_etf()
    print(f"成功获取数据: {result}")
except Exception as e:
    print(f"错误: {e}")

print("\n测试 get_china_etf 函数...")
try:
    result = get_china_etf()
    print(f"成功获取数据: {result}")
except Exception as e:
    print(f"错误: {e}")
