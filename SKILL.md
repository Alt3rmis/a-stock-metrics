# A股市场数据指标 Skill

## 概述

本 Skill 用于获取 A 股市场多空情绪相关的数据指标，提供原子化的数据获取接口。

## 可用指标列表

| 指标ID | 函数名 | 指标名称 | 数据源 | 多空判断逻辑 |
|--------|--------|----------|--------|--------------|
| `margin` | `get_margin()` | 融资融券 | akshare | 近N日余额变化 > 0 → 多 |
| `if_main` | `get_futures_if()` | 沪深300期货 | akshare | 涨跌幅 > 0 → 多 |
| `im_main` | `get_futures_im()` | 中证1000期货 | akshare | 涨跌幅 > 0 → 多 |
| `lhb` | `get_lhb()` | 龙虎榜 | 东方财富 | 机构净买入 > 0 → 多 |
| `limitup` | `get_limitup()` | 涨停板环境 | akshare | 环境评分 > 0 → 多 |
| `industry_flow` | `get_industry_flow()` | 行业资金流 | akshare | 无直接信号 |

## 安装

```bash
cd a-stock-metrics
pip install -e .
```

## API 使用方法

### 基础导入

```python
from astock_metrics import (
    get_margin,
    get_futures_if,
    get_futures_im,
    get_lhb,
    get_limitup,
    get_industry_flow
)
```

### 1. 获取融资融券数据

```python
from astock_metrics import get_margin

result = get_margin(days=3)
print(f"信号: {result['signal']}")      # "多"/"空"/"中性"
print(f"分数: {result['score']}")       # 1/-1/0
print(f"变化额: {result['delta']}")     # 余额变化
```

**参数**: `days` - 计算变化的天数（默认3）

### 2. 获取股指期货数据

```python
from astock_metrics import get_futures_if, get_futures_im

# 沪深300期货
if_result = get_futures_if()
print(f"涨跌幅: {if_result['pct_change']}%")
print(f"信号: {if_result['signal']}")

# 中证1000期货
im_result = get_futures_im()
print(f"涨跌幅: {im_result['pct_change']}%")
print(f"信号: {im_result['signal']}")
```

### 3. 获取龙虎榜数据

```python
from astock_metrics import get_lhb

result = get_lhb(date="20250310")
print(f"机构净买入: {result['total_net']}")
print(f"信号: {result['signal']}")
print(f"热门做多行业: {result['hot_buy']}")
```

**参数**: 
- `date` - 日期 (YYYYMMDD格式)
- `top_n` - 热门行业数量（默认5）

### 4. 获取涨停板数据

```python
from astock_metrics import get_limitup

result = get_limitup(date="20250310")
print(f"涨停家数: {result['struct']['total_zt']}")
print(f"最高板: {result['struct']['max_lb']}板")
print(f"环境: {result['env_desc']}")
print(f"梯队: {result['tier']['tier_quality']}")
```

**参数**:
- `date` - 日期 (YYYYMMDD格式)
- `top_n_industry` - 行业TOP N（默认5）

### 5. 获取行业资金流

```python
from astock_metrics import get_industry_flow

result = get_industry_flow(top_n=5)
for item in result['top_in']:
    print(f"{item['行业']}: {item['净额']:+.2f}亿")
```

**参数**: `top_n` - 返回TOP N（默认5）

## 返回数据结构

所有 `get_*` 函数返回统一格式的字典：

```python
{
    "metric_id": str,       # 指标ID
    "name": str,            # 中文名称
    "signal": str,          # "多"/"空"/"中性"
    "score": int,           # 1/-1/0
    "error": str | None,    # 错误信息（如果有）
    # ... 其他指标特定字段
}
```

### 各指标详细字段

#### margin (融资融券)
```python
{
    "latest_date": str,     # 最新日期
    "start": float,         # 起始余额
    "end": float,           # 当前余额
    "delta": float,         # 变化额
    "days": int,            # 天数
    "signal_desc": str,     # 信号描述
}
```

#### if_main / im_main (期货)
```python
{
    "date": str,            # 日期
    "pct_change": float,    # 涨跌幅%
}
```

#### lhb (龙虎榜)
```python
{
    "date": str,            # 日期
    "total_net": float,     # 机构净买入总额
    "record_count": int,    # 上榜记录数
    "hot_buy": dict,        # 热门做多行业
    "hot_sell": dict,       # 机构净卖出行业
}
```

#### limitup (涨停板)
```python
{
    "date": str,            # 日期
    "env_desc": str,        # 环境描述
    "env_score": int,       # 环境评分
    "struct": {
        "total_zt": int,    # 涨停家数
        "max_lb": int,      # 最高板
        "lb_dist": dict,    # 连板分布
        "industry_top": dict,  # 行业集中度
    },
    "breaks": {
        "total_zb": int,    # 炸板家数
    },
    "tier": {
        "tier_quality": str,    # 梯队质量描述
        "active_tiers": list,   # 活跃板位
        "tier_count": int,      # 梯队数量
    },
    "graduation": {
        "graduation_status": str,   # 毕业照状态
        "graduation_score": int,    # 毕业照分数
        "graduation_signals": list, # 毕业照信号
    },
}
```

#### industry_flow (行业资金流)
```python
{
    "top_in": [             # 净流入TOP N
        {"行业": str, "净额": float, "流入资金": float, ...},
        ...
    ],
    "top_out": [            # 净流出TOP N
        {"行业": str, "净额": float, "流入资金": float, ...},
        ...
    ],
}
```

## 常见使用场景

### 场景1: 快速判断大盘方向

```python
from astock_metrics import get_margin, get_futures_if, get_futures_im

# 获取多个指标
margin = get_margin(days=3)
if_main = get_futures_if()
im_main = get_futures_im()

# 计算多空分数
long_score = sum(r['score'] for r in [margin, if_main, im_main] if r['score'] > 0)
short_score = sum(abs(r['score']) for r in [margin, if_main, im_main] if r['score'] < 0)

if long_score > short_score * 2:
    print("多方占优")
elif short_score > long_score * 2:
    print("空方占优")
else:
    print("震荡/分歧")
```

### 场景2: 分析涨停板情绪

```python
from astock_metrics import get_limitup

result = get_limitup(date="20250310")
if result['error'] is None:
    struct = result['struct']
    print(f"涨停家数: {struct['total_zt']}")
    print(f"最高板: {struct['max_lb']}板")
    print(f"环境: {result['env_desc']}")
    print(f"梯队: {result['tier']['tier_quality']}")
else:
    print(f"获取失败: {result['error']}")
```

### 场景3: 查看机构资金动向

```python
from astock_metrics import get_lhb

result = get_lhb(date="20250310")
if result['error'] is None:
    total_net = result['total_net']
    if total_net > 0:
        print(f"机构净买入: {total_net:,.0f}")
    else:
        print(f"机构净卖出: {abs(total_net):,.0f}")
    print(f"信号: {result['signal_desc']}")
```

## 错误处理

所有函数在出错时会返回包含 `error` 字段的字典：

```python
from astock_metrics import get_limitup

result = get_limitup(date="20250310")

if result['error'] is None:
    # 处理成功结果
    print(result['signal'])
else:
    # 处理错误
    print(f"获取失败: {result['error']}")
```

## 注意事项

1. **日期格式**: 统一使用 `YYYYMMDD` 格式，如 `"20250310"`
2. **交易时间**: 部分数据仅在交易日有值，非交易日可能返回错误
3. **网络依赖**: 需要访问 akshare 和东方财富 API，请确保网络畅通
4. **数据延迟**: 融资融券数据通常滞后1-2个交易日

## 低级API

如果需要更细粒度的控制，可以使用底层函数：

```python
from astock_metrics.margin import fetch_total_margin_change, judge_margin_signal
from astock_metrics.futures import fetch_if_main, fetch_im_main
from astock_metrics.lhb import fetch_lhb_institution_flow, analyze_lhb_hot_industries
from astock_metrics.limitup import (
    analyze_limitup_structure,
    analyze_limitup_break,
    analyze_tier_structure,
    analyze_sector_graduation,
    score_limitup_env
)
from astock_metrics.industry import fetch_industry_fund_flow_3d
```

## 完整示例

```python
"""
完整的A股市场情绪分析示例
"""
from astock_metrics import (
    get_margin,
    get_futures_if,
    get_futures_im,
    get_lhb,
    get_limitup,
    get_industry_flow
)

def analyze_market(date: str = None):
    print("=" * 50)
    print("A股市场情绪分析")
    print("=" * 50)

    # 1. 融资融券
    margin = get_margin(days=3)
    print(f"\n【融资融券】")
    if margin['error'] is None:
        print(f"  余额变化: {margin['delta']:+,.0f}")
        print(f"  信号: {margin['signal_desc']}")
    else:
        print(f"  获取失败: {margin['error']}")

    # 2. 股指期货
    print(f"\n【股指期货】")
    for name, func in [("沪深300", get_futures_if), ("中证1000", get_futures_im)]:
        result = func()
        if result['error'] is None:
            print(f"  {name}: {result['pct_change']:+.2f}% → {result['signal']}")
        else:
            print(f"  {name}: 获取失败")

    # 3. 龙虎榜
    if date:
        print(f"\n【龙虎榜】")
        lhb = get_lhb(date=date)
        if lhb['error'] is None:
            print(f"  机构净买入: {lhb['total_net']:,.0f}")
            print(f"  信号: {lhb['signal_desc']}")
        else:
            print(f"  获取失败: {lhb['error']}")

    # 4. 涨停板
    if date:
        print(f"\n【涨停板】")
        limitup = get_limitup(date=date)
        if limitup['error'] is None:
            struct = limitup['struct']
            print(f"  涨停家数: {struct['total_zt']}")
            print(f"  最高板: {struct['max_lb']}板")
            print(f"  环境: {limitup['env_desc']}")
        else:
            print(f"  获取失败: {limitup['error']}")

    # 5. 计算综合分数
    results = [margin, get_futures_if(), get_futures_im()]
    if date:
        results.extend([get_lhb(date=date), get_limitup(date=date)])

    valid_results = [r for r in results if r.get('error') is None]
    long_score = sum(r['score'] for r in valid_results if r['score'] > 0)
    short_score = sum(abs(r['score']) for r in valid_results if r['score'] < 0)

    print(f"\n【多空分数】")
    print(f"  多方: {long_score}")
    print(f"  空方: {short_score}")

    if long_score >= short_score * 2:
        conclusion = "多方占优"
    elif short_score >= long_score * 2:
        conclusion = "空方占优"
    else:
        conclusion = "震荡/分歧"

    print(f"\n【结论】{conclusion}")

if __name__ == "__main__":
    import sys
    date = sys.argv[1] if len(sys.argv) > 1 else None
    analyze_market(date)
```
