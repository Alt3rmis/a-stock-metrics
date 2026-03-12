#!/usr/bin/env python3
"""测试外部数据源采集模块"""

from astock_metrics.data.external import fetch_china_etf, get_china_etf


def test_fetch_china_etf():
    """测试获取中概ETF数据"""
    print("测试 fetch_china_etf 函数...")
    result = fetch_china_etf()
    print(f"结果: {result}")
    print(f"日期: {result['date']}")
    print(f"涨跌幅: {result['pct_change']:.2f}%")
    print(f"信号: {result['signal']}")
    print(f"信号值: {result['signal_value']}")
    if 'detail' in result:
        print(f"详细数据: {result['detail']}")
    print()


def test_get_china_etf():
    """测试获取中概ETF数据（统一接口）"""
    print("测试 get_china_etf 函数...")
    result = get_china_etf()
    print(f"结果: {result}")
    print(f"指标ID: {result['metric_id']}")
    print(f"名称: {result['name']}")
    print(f"信号: {result['signal']}")
    print(f"信号值: {result['signal_value']}")
    print(f"权重: {result['weight']}")
    print(f"得分: {result['score']:.2f}")
    print(f"详细数据: {result['detail']}")
    print(f"错误: {result['error']}")
    print()


if __name__ == "__main__":
    print("开始测试外部数据源采集模块...\n")
    test_fetch_china_etf()
    test_get_china_etf()
    print("测试完成！")
