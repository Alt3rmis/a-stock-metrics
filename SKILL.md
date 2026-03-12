# A股市场数据指标 Skill

## 概述

本 Skill 用于获取 A 股市场多空情绪相关的数据指标，提供原子化的数据获取接口，并支持指标评分和综合决策。

## 项目结构

项目采用三层架构：

1. **数据采集层（Data Layer）**：负责从各个数据源获取原始数据
2. **指标评分层（Metrics Layer）**：负责计算各类型指标的综合评分
3. **综合决策层（Decision Layer）**：负责分析市场方向，生成最终信号

## 可用指标列表

### 指数预期指标

| 指标ID | 函数名 | 指标名称 | 数据源 | 权重 | 多空判断逻辑 |
|--------|--------|----------|--------|------|--------------|
| `a50` | `get_futures_a50()` | A50期指 | 模拟数据 | 1 | 涨跌幅 > 0 → 多 |
| `if_main` | `get_futures_if()` | 沪深300期指 | akshare | 1 | 涨跌幅 > 0 → 多 |
| `im_main` | `get_futures_im()` | 中证1000期指 | akshare | 1 | 涨跌幅 > 0 → 多 |

### 资金指标

| 指标ID | 函数名 | 指标名称 | 数据源 | 权重 | 多空判断逻辑 |
|--------|--------|----------|--------|------|--------------|
| `margin` | `get_margin()` | 融资融券 | akshare | 1 | 近N日余额变化 > 0 → 多 |
| `northbound` | `get_northbound()` | 北向资金 | akshare | 1 | 净流入 > 0 → 多 |
| `industry_flow` | `get_industry_flow()` | 行业资金流 | akshare | 1 | 总净流入 > 0 → 多 |
| `lhb` | `get_lhb()` | 龙虎榜机构 | 东方财富 | 1 | 机构净买入 > 0 → 多 |

### 情绪指标

| 指标ID | 函数名 | 指标名称 | 数据源 | 权重 | 多空判断逻辑 |
|--------|--------|----------|--------|------|--------------|
| `limitup` | `get_limitup()` | 涨停板环境 | akshare | 1 | 环境评分 > 0 → 多 |
| `limitup_premium` | `get_limitup_premium()` | 涨停溢价 | 模拟数据 | 1 | 溢价 > 0.03 → 多 |
| `break_rate` | `get_break_rate()` | 炸板率 | akshare | 1 | 炸板率 < 0.3 → 多 |

### 外围指标

| 指标ID | 函数名 | 指标名称 | 数据源 | 权重 | 多空判断逻辑 |
|--------|--------|----------|--------|------|--------------|
| `singapore_a50` | `get_singapore_a50()` | 新加坡A50 | 模拟数据 | 0.1 | 涨跌幅 > 0 → 多 |
| `nasdaq` | `get_nasdaq()` | 纳斯达克 | akshare | 0.1 | 涨跌幅 > 0 → 多 |
| `usd_index` | `get_usd_index()` | 美元指数 | 模拟数据 | 0.1 | 涨跌幅 < 0 → 多 |
| `china_etf` | `get_china_etf()` | 中概ETF | 模拟数据 | 0.1 | 涨跌幅 > 0 → 多 |

## 安装

```bash
cd a-stock-metrics
pip install -e .
```

## API 使用方法

### 基础导入

```python
# 数据采集层
from astock_metrics.data import (
    get_futures_a50, get_futures_if, get_futures_im,
    get_margin, get_northbound, get_industry_flow, get_lhb,
    get_limitup, get_limitup_premium, get_break_rate,
    get_singapore_a50, get_nasdaq, get_usd_index, get_china_etf
)

# 指标评分层
from metrics import (
    calculate_index_metrics, calculate_fund_metrics,
    calculate_sentiment_metrics, calculate_external_metrics
)

# 综合决策层
from decision import analyze_market_direction, get_market_signal
```

### 1. 获取指数预期指标

```python
from astock_metrics.data.futures import get_futures_a50, get_futures_if, get_futures_im

# A50期指
a50_result = get_futures_a50()
print(f"A50期指: {a50_result['detail']['pct_change']:+.2f}% | {a50_result['signal']} | Score: {a50_result['score']}")

# 沪深300期指
if_result = get_futures_if()
print(f"沪深300期指: {if_result['detail']['pct_change']:+.2f}% | {if_result['signal']} | Score: {if_result['score']}")

# 中证1000期指
im_result = get_futures_im()
print(f"中证1000期指: {im_result['detail']['pct_change']:+.2f}% | {im_result['signal']} | Score: {im_result['score']}")
```

### 2. 获取资金指标

```python
from astock_metrics.data.margin import get_margin
from astock_metrics.data.northbound import get_northbound
from astock_metrics.data.industry_flow import get_industry_flow
from astock_metrics.data.lhb import get_lhb

# 融资融券
margin_result = get_margin(days=3)
print(f"融资融券: {margin_result['signal']} | Score: {margin_result['score']}")
print(f"  余额变化: {margin_result['detail']['delta']:+,.0f}")

# 北向资金
northbound_result = get_northbound()
print(f"北向资金: {northbound_result['signal']} | Score: {northbound_result['score']}")
print(f"  净流入: {northbound_result['detail']['net_flow']:+,.0f}")

# 行业资金流
industry_flow_result = get_industry_flow()
print(f"行业资金流: {industry_flow_result['signal']} | Score: {industry_flow_result['score']}")
print(f"  总净流入: {industry_flow_result['detail']['total_inflow']:+,.0f}")

# 龙虎榜机构
lhb_result = get_lhb(date="20250310")
print(f"龙虎榜机构: {lhb_result['signal']} | Score: {lhb_result['score']}")
print(f"  机构净买入: {lhb_result['detail']['total_net']:+,.0f}")
```

### 3. 获取情绪指标

```python
from astock_metrics.data.limitup import get_limitup, get_limitup_premium, get_break_rate

# 涨停板环境
limitup_result = get_limitup(date="20250310")
print(f"涨停板环境: {limitup_result['signal']} | Score: {limitup_result['score']}")
print(f"  涨停家数: {limitup_result['detail']['total_zt']}")
print(f"  最高板: {limitup_result['detail']['max_lb']}板")

# 涨停溢价
premium_result = get_limitup_premium(date="20250310")
print(f"涨停溢价: {premium_result['signal']} | Score: {premium_result['score']}")
print(f"  溢价率: {premium_result['detail']['premium']:.2%}")

# 炸板率
break_rate_result = get_break_rate(date="20250310")
print(f"炸板率: {break_rate_result['signal']} | Score: {break_rate_result['score']}")
print(f"  炸板率: {break_rate_result['detail']['break_rate']:.2%}")
```

### 4. 获取外围指标

```python
from astock_metrics.data.external import get_singapore_a50, get_nasdaq, get_usd_index, get_china_etf

# 新加坡A50
sg_a50_result = get_singapore_a50()
print(f"新加坡A50: {sg_a50_result['signal']} | Score: {sg_a50_result['score']}")

# 纳斯达克
nasdaq_result = get_nasdaq()
print(f"纳斯达克: {nasdaq_result['signal']} | Score: {nasdaq_result['score']}")

# 美元指数
usd_result = get_usd_index()
print(f"美元指数: {usd_result['signal']} | Score: {usd_result['score']}")

# 中概ETF
china_etf_result = get_china_etf()
print(f"中概ETF: {china_etf_result['signal']} | Score: {china_etf_result['score']}")
```

### 5. 计算指标评分

```python
from metrics import calculate_index_metrics, calculate_fund_metrics, calculate_sentiment_metrics, calculate_external_metrics

# 指数指标评分
index_metrics = [get_futures_a50(), get_futures_if(), get_futures_im()]
index_score = calculate_index_metrics(index_metrics)
print(f"指数指标综合: {index_score['signal']} | Score: {index_score['score']}")

# 资金指标评分
fund_metrics = [get_margin(), get_northbound(), get_industry_flow(), get_lhb(date="20250310")]
fund_score = calculate_fund_metrics(fund_metrics)
print(f"资金指标综合: {fund_score['signal']} | Score: {fund_score['score']}")

# 情绪指标评分
sentiment_metrics = [get_limitup(date="20250310"), get_limitup_premium(date="20250310"), get_break_rate(date="20250310")]
sentiment_score = calculate_sentiment_metrics(sentiment_metrics)
print(f"情绪指标综合: {sentiment_score['signal']} | Score: {sentiment_score['score']}")

# 外部指标评分
external_metrics = [get_singapore_a50(), get_nasdaq(), get_usd_index(), get_china_etf()]
external_score = calculate_external_metrics(external_metrics)
print(f"外部指标综合: {external_score['signal']} | Score: {external_score['score']}")
```

### 6. 分析市场方向

```python
from decision import analyze_market_direction, get_market_signal

# 收集所有指标
all_metrics = [
    # 指数预期
    get_futures_a50(), get_futures_if(), get_futures_im(),
    # 资金
    get_margin(), get_northbound(), get_industry_flow(), get_lhb(date="20250310"),
    # 情绪
    get_limitup(date="20250310"), get_limitup_premium(date="20250310"), get_break_rate(date="20250310"),
    # 外围
    get_singapore_a50(), get_nasdaq(), get_usd_index(), get_china_etf()
]

# 分析市场方向
market_result = analyze_market_direction(all_metrics)
print(f"市场方向综合: {market_result['signal']} | Score: {market_result['score']}")
print(f"  平均分数: {market_result['detail']['avg_score']:.2f}")
print(f"  有效指标数: {market_result['detail']['valid_count']}")

# 按类型查看统计
for metric_type, stats in market_result['detail']['type_stats'].items():
    print(f"  {metric_type}: 平均分数 {stats['avg_score']:.2f}, 信号: {stats['signals']}")

# 获取市场信号
market_signal = get_market_signal(all_metrics)
print(f"最终市场信号: {market_signal}")
```

## 返回数据结构

所有指标函数返回统一格式的字典：

```python
{
    "metric_id": "a50",       # 指标ID
    "name": "A50期指",        # 指标名称
    "signal": "多",           # 信号（多/空/中性）
    "signal_value": 1,         # 信号值（1/-1/0）
    "weight": 1,              # 权重
    "score": 1,               # 评分（signal_value * weight）
    "detail": {},             # 详细信息（各指标不同）
    "error": None             # 错误信息（如果有）
}
```

### 各指标详细字段

#### 指数预期指标（a50, if_main, im_main）
```python
{
    "date": "2026-03-12",    # 日期
    "pct_change": 0.5         # 涨跌幅%
}
```

#### 资金指标

**margin（融资融券）**
```python
{
    "latest_date": "2026-03-12",  # 最新日期
    "start": 1234567890,           # 起始余额
    "end": 1234567890,             # 当前余额
    "delta": 10000000,             # 变化额
    "days": 3,                      # 天数
    "signal_desc": "融资余额增加 → 偏多"  # 信号描述
}
```

**northbound（北向资金）**
```python
{
    "date": "2026-03-12",    # 日期
    "net_flow": 1000000000    # 净流入
}
```

**industry_flow（行业资金流）**
```python
{
    "date": "2026-03-12",    # 日期
    "total_inflow": 5000000000,  # 总净流入
    "top_industries": {}       # 热门行业
}
```

**lhb（龙虎榜机构）**
```python
{
    "date": "20250310",       # 日期
    "total_net": 123456789,    # 机构净买入总额
    "record_count": 50,        # 上榜记录数
    "signal_desc": "机构整体净买入 → 偏多",  # 信号描述
    "hot_buy": {},             # 热门做多行业
    "hot_sell": {}             # 机构净卖出行业
}
```

#### 情绪指标

**limitup（涨停板环境）**
```python
{
    "date": "20250310",       # 日期
    "env_desc": "涨停结构强，适合接力",  # 环境描述
    "total_zt": 85,            # 涨停家数
    "max_lb": 5,               # 最高板
    "total_zb": 15,            # 炸板家数
    "break_ratio": 0.15,       # 炸板率
    "tier_quality": "梯队结构完整，接力顺畅",  # 梯队质量
    "graduation_status": "梯队正常"  # 毕业照状态
}
```

**limitup_premium（涨停溢价）**
```python
{
    "date": "20250310",       # 日期
    "premium": 0.05            # 溢价率
}
```

**break_rate（炸板率）**
```python
{
    "date": "20250310",       # 日期
    "total_zt": 85,            # 涨停家数
    "total_zb": 15,            # 炸板家数
    "break_rate": 0.15         # 炸板率
}
```

#### 外围指标（singapore_a50, nasdaq, usd_index, china_etf）
```python
{
    "date": "2026-03-12",    # 日期
    "pct_change": 0.3          # 涨跌幅%
}
```

## 常见使用场景

### 场景1: 快速判断大盘方向

```python
from astock_metrics.data import (
    get_futures_a50, get_futures_if, get_futures_im,
    get_margin, get_northbound, get_industry_flow, get_lhb,
    get_limitup, get_limitup_premium, get_break_rate,
    get_singapore_a50, get_nasdaq, get_usd_index, get_china_etf
)
from decision import analyze_market_direction

# 收集所有指标
all_metrics = [
    get_futures_a50(), get_futures_if(), get_futures_im(),
    get_margin(), get_northbound(), get_industry_flow(), get_lhb(date="20250310"),
    get_limitup(date="20250310"), get_limitup_premium(date="20250310"), get_break_rate(date="20250310"),
    get_singapore_a50(), get_nasdaq(), get_usd_index(), get_china_etf()
]

# 分析市场方向
result = analyze_market_direction(all_metrics)
print(f"市场方向: {result['signal']}")
print(f"综合评分: {result['score']}")
print(f"平均分数: {result['detail']['avg_score']:.2f}")

# 按类型查看
for metric_type, stats in result['detail']['type_stats'].items():
    print(f"{metric_type}: 平均分数 {stats['avg_score']:.2f}, 信号: {stats['signals']}")
```

### 场景2: 分析市场情绪

```python
from astock_metrics.data import get_limitup, get_limitup_premium, get_break_rate
from metrics import calculate_sentiment_metrics

# 获取情绪相关指标
sentiment_metrics = [
    get_limitup(date="20250310"),
    get_limitup_premium(date="20250310"),
    get_break_rate(date="20250310")
]

# 计算情绪综合评分
sentiment_score = calculate_sentiment_metrics(sentiment_metrics)
print(f"情绪综合: {sentiment_score['signal']} | Score: {sentiment_score['score']}")

# 查看详细信息
for metric in sentiment_metrics:
    print(f"{metric['name']}: {metric['signal']} | Score: {metric['score']}")
    if metric['metric_id'] == 'limitup':
        print(f"  涨停家数: {metric['detail']['total_zt']}")
        print(f"  最高板: {metric['detail']['max_lb']}板")
    elif metric['metric_id'] == 'break_rate':
        print(f"  炸板率: {metric['detail']['break_rate']:.2%}")
```

## 错误处理

所有函数在出错时会返回包含 `error` 字段的字典：

```python
from astock_metrics.data import get_limitup

result = get_limitup(date="20250310")

if result['error'] is None:
    # 处理成功结果
    print(f"涨停板环境: {result['signal']}")
else:
    # 处理错误
    print(f"获取失败: {result['error']}")
```

## 注意事项

1. **日期格式**: 统一使用 `YYYYMMDD` 格式，如 `"20250310"`
2. **交易时间**: 部分数据仅在交易日有值，非交易日可能返回错误
3. **网络依赖**: 需要访问 akshare 和东方财富 API，请确保网络畅通
4. **数据延迟**: 融资融券数据通常滞后1-2个交易日
5. **模拟数据**: 部分指标（如A50期指、新加坡A50、美元指数、中概ETF）使用模拟数据，实际使用时需要替换为真实数据源

## 完整示例

```python
"""
完整的A股市场情绪分析示例
"""
from astock_metrics.data import (
    get_futures_a50, get_futures_if, get_futures_im,
    get_margin, get_northbound, get_industry_flow, get_lhb,
    get_limitup, get_limitup_premium, get_break_rate,
    get_singapore_a50, get_nasdaq, get_usd_index, get_china_etf
)
from metrics import (
    calculate_index_metrics, calculate_fund_metrics,
    calculate_sentiment_metrics, calculate_external_metrics
)
from decision import analyze_market_direction

def analyze_market(date: str = None):
    print("=" * 70)
    print("A股市场情绪分析")
    print("=" * 70)

    # 1. 指数预期
    print(f"\n【指数预期】")
    index_metrics = []
    for name, func in [
        ("A50期指", get_futures_a50),
        ("沪深300期指", get_futures_if),
        ("中证1000期指", get_futures_im)
    ]:
        result = func()
        index_metrics.append(result)
        if result['error'] is None:
            print(f"  {name}: {result['detail']['pct_change']:+.2f}% → {result['signal']} (Score: {result['score']})")
        else:
            print(f"  {name}: 获取失败 - {result['error']}")
    
    # 2. 资金
    print(f"\n【资金】")
    fund_metrics = []
    
    margin = get_margin(days=3)
    fund_metrics.append(margin)
    if margin['error'] is None:
        print(f"  融资融券: {margin['signal']} (Score: {margin['score']})")
        print(f"    余额变化: {margin['detail']['delta']:+,.0f}")
    else:
        print(f"  融资融券: 获取失败 - {margin['error']}")
    
    northbound = get_northbound()
    fund_metrics.append(northbound)
    if northbound['error'] is None:
        print(f"  北向资金: {northbound['signal']} (Score: {northbound['score']})")
        print(f"    净流入: {northbound['detail']['net_flow']:+,.0f}")
    else:
        print(f"  北向资金: 获取失败 - {northbound['error']}")
    
    industry_flow = get_industry_flow()
    fund_metrics.append(industry_flow)
    if industry_flow['error'] is None:
        print(f"  行业资金流: {industry_flow['signal']} (Score: {industry_flow['score']})")
        print(f"    总净流入: {industry_flow['detail']['total_inflow']:+,.0f}")
    else:
        print(f"  行业资金流: 获取失败 - {industry_flow['error']}")
    
    if date:
        lhb = get_lhb(date=date)
        fund_metrics.append(lhb)
        if lhb['error'] is None:
            print(f"  龙虎榜机构: {lhb['signal']} (Score: {lhb['score']})")
            print(f"    机构净买入: {lhb['detail']['total_net']:+,.0f}")
        else:
            print(f"  龙虎榜机构: 获取失败 - {lhb['error']}")
    
    # 3. 情绪
    print(f"\n【情绪】")
    sentiment_metrics = []
    
    if date:
        limitup = get_limitup(date=date)
        sentiment_metrics.append(limitup)
        if limitup['error'] is None:
            print(f"  涨停板环境: {limitup['signal']} (Score: {limitup['score']})")
            print(f"    涨停家数: {limitup['detail']['total_zt']}")
            print(f"    最高板: {limitup['detail']['max_lb']}板")
            print(f"    炸板率: {limitup['detail']['break_ratio']:.2%}")
        else:
            print(f"  涨停板环境: 获取失败 - {limitup['error']}")
        
        premium = get_limitup_premium(date=date)
        sentiment_metrics.append(premium)
        if premium['error'] is None:
            print(f"  涨停溢价: {premium['signal']} (Score: {premium['score']})")
            print(f"    溢价率: {premium['detail']['premium']:.2%}")
        else:
            print(f"  涨停溢价: 获取失败 - {premium['error']}")
        
        break_rate = get_break_rate(date=date)
        sentiment_metrics.append(break_rate)
        if break_rate['error'] is None:
            print(f"  炸板率: {break_rate['signal']} (Score: {break_rate['score']})")
            print(f"    炸板率: {break_rate['detail']['break_rate']:.2%}")
        else:
            print(f"  炸板率: 获取失败 - {break_rate['error']}")
    
    # 4. 外围
    print(f"\n【外围】")
    external_metrics = []
    for name, func in [
        ("新加坡A50", get_singapore_a50),
        ("纳斯达克", get_nasdaq),
        ("美元指数", get_usd_index),
        ("中概ETF", get_china_etf)
    ]:
        result = func()
        external_metrics.append(result)
        if result['error'] is None:
            print(f"  {name}: {result['signal']} (Score: {result['score']})")
            print(f"    涨跌幅: {result['detail']['pct_change']:+.2f}%")
        else:
            print(f"  {name}: 获取失败 - {result['error']}")
    
    # 5. 计算各类型综合评分
    print(f"\n【综合评分】")
    if index_metrics:
        index_score = calculate_index_metrics(index_metrics)
        print(f"  指数预期: {index_score['signal']} (Score: {index_score['score']})")
    
    if fund_metrics:
        fund_score = calculate_fund_metrics(fund_metrics)
        print(f"  资金: {fund_score['signal']} (Score: {fund_score['score']})")
    
    if sentiment_metrics:
        sentiment_score = calculate_sentiment_metrics(sentiment_metrics)
        print(f"  情绪: {sentiment_score['signal']} (Score: {sentiment_score['score']})")
    
    if external_metrics:
        external_score = calculate_external_metrics(external_metrics)
        print(f"  外围: {external_score['signal']} (Score: {external_score['score']})")
    
    # 6. 市场方向综合分析
    print(f"\n【市场方向综合】")
    all_metrics = index_metrics + fund_metrics + sentiment_metrics + external_metrics
    market_result = analyze_market_direction(all_metrics)
    print(f"  信号: {market_result['signal']}")
    print(f"  综合评分: {market_result['score']}")
    print(f"  平均分数: {market_result['detail']['avg_score']:.2f}")
    print(f"  有效指标数: {market_result['detail']['valid_count']}/{market_result['detail']['metrics_count']}")
    
    # 7. 按类型统计
    print(f"\n【类型统计】")
    for metric_type, stats in market_result['detail']['type_stats'].items():
        print(f"  {metric_type}: 平均分数 {stats['avg_score']:.2f}, 信号: {stats['signals']}")

if __name__ == "__main__":
    import sys
    date = sys.argv[1] if len(sys.argv) > 1 else "20250310"
    analyze_market(date)
```