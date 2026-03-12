# A股市场数据指标获取包

提供原子化的数据获取接口，每个指标可独立调用。

## 安装

```bash
pip install -e .
```

## 快速开始

```python
from astock_metrics import (
    get_margin,
    get_futures_if,
    get_futures_im,
    get_lhb,
    get_limitup,
    get_industry_flow
)

# 获取融资融券数据
margin = get_margin(days=3)
print(f"信号: {margin['signal']}, 变化: {margin['delta']:+,.0f}")

# 获取沪深300期货信号
futures = get_futures_if()
print(f"涨跌幅: {futures['pct_change']:+.2f}%, 信号: {futures['signal']}")

# 获取涨停板数据
limitup = get_limitup(date="20250310")
print(f"涨停家数: {limitup['struct']['total_zt']}, 环境: {limitup['env_desc']}")
```

## 可用指标

| 函数 | 指标名称 | 多空判断 |
|------|----------|----------|
| `get_margin()` | 融资融券 | 余额变化 > 0 → 多 |
| `get_futures_if()` | 沪深300期货 | 涨跌幅 > 0 → 多 |
| `get_futures_im()` | 中证1000期货 | 涨跌幅 > 0 → 多 |
| `get_lhb()` | 龙虎榜 | 机构净买入 > 0 → 多 |
| `get_limitup()` | 涨停板环境 | 环境评分 > 0 → 多 |
| `get_industry_flow()` | 行业资金流 | 无直接信号 |

## 返回数据结构

所有 `get_*` 函数返回统一格式的字典：

```python
{
    "metric_id": "指标ID",
    "name": "中文名称",
    "signal": "多" | "空" | "中性",
    "score": 1 | -1 | 0,
    "error": None | "错误信息",
    # ... 其他指标特定字段
}
```

## 依赖

- akshare >= 1.12.0
- pandas >= 2.0.0
- requests >= 2.28.0
