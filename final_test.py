#!/usr/bin/env python3
"""最终测试脚本"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

print("开始测试...")
print(f"Python版本: {sys.version}")
print(f"当前目录: {os.getcwd()}")

# 测试导入
try:
    from astock_metrics.data.external import fetch_china_etf, get_china_etf
    print("成功导入模块")
except Exception as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)

# 测试fetch_china_etf函数
print("\n测试fetch_china_etf函数...")
try:
    result = fetch_china_etf()
    print(f"函数返回类型: {type(result)}")
    print(f"函数返回值: {result}")
except Exception as e:
    print(f"调用fetch_china_etf失败: {e}")

# 测试get_china_etf函数
print("\n测试get_china_etf函数...")
try:
    result = get_china_etf()
    print(f"函数返回类型: {type(result)}")
    print(f"函数返回值: {result}")
except Exception as e:
    print(f"调用get_china_etf失败: {e}")

print("\n测试完成!")
