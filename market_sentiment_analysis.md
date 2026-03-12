---
name: market-sentiment-analysis
description: "A股市场情绪综合分析技能：自动获取市场多空情绪相关的14个指标数据，从指数预期、资金、情绪、外围四个维度生成结构化分析报告，含市场方向判断和操作建议。支持：(1) 市场情绪实时分析 (2) 多维度指标综合评估 (3) 市场方向预测 (4) 操作策略建议。适用于用户问'市场情绪如何'、'大盘走势分析'、'今天市场怎么样'等请求。"
---

# A股市场情绪综合分析

## 数据获取

运行 `scripts/analyze_market_sentiment.py` 获取市场情绪数据（需要安装 akshare 依赖）：

```bash
python scripts/analyze_market_sentiment.py [--date <日期>]
```

- 支持指定日期（如 `20250310`），默认使用当日
- 自动获取14个市场情绪指标数据
- 输出结构化的市场情绪分析报告

## 分析框架（4维度14指标）

获取数据后，按以下框架生成分析报告：

### 一、指数预期（3指标）
1. **A50期指** — 涨跌幅、多空信号、评分
2. **沪深300期指** — 涨跌幅、多空信号、评分
3. **中证1000期指** — 涨跌幅、多空信号、评分

### 二、资金面（4指标）
4. **融资融券** — 余额变化、多空信号、评分
5. **北向资金** — 净流入、多空信号、评分
6. **行业资金流** — 总净流入、多空信号、评分
7. **龙虎榜机构** — 机构净买入、多空信号、评分

### 三、情绪面（3指标）
8. **涨停板环境** — 涨停家数、最高板、炸板率、多空信号、评分
9. **涨停溢价** — 溢价率、多空信号、评分
10. **炸板率** — 炸板率、多空信号、评分

### 四、外围市场（4指标）
11. **新加坡A50** — 涨跌幅、多空信号、评分
12. **纳斯达克** — 涨跌幅、多空信号、评分
13. **美元指数** — 涨跌幅、多空信号、评分
14. **中概ETF** — 涨跌幅、多空信号、评分

## 综合分析

基于上述14个指标的评分，进行综合分析：

### 1. 各维度评分
- **指数预期维度** — 综合3个指数指标的评分
- **资金面维度** — 综合4个资金指标的评分
- **情绪面维度** — 综合3个情绪指标的评分
- **外围市场维度** — 综合4个外围指标的评分

### 2. 市场方向判断
- **综合评分** — 所有指标的加权平均分
- **市场信号** — 多/空/中性
- **信号强度** — 强/中/弱

### 3. 操作建议
- **短期策略** — 激进/稳健/谨慎
- **仓位建议** — 高/中/低
- **关注方向** — 推荐关注的行业或板块

## 输出格式

报告使用 Markdown 结构，每个维度用 ### 标题。关键数据**加粗**。结尾必须包含：

> ⚠️ **免责声明**：以上分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。数据来源于公开市场，可能存在延迟。

## 示例输出

### 市场情绪分析报告

**日期**: 2025-03-10

#### 一、指数预期
- **A50期指**: +0.50% → **多** (Score: 1.0)
- **沪深300期指**: +0.85% → **多** (Score: 1.0)
- **中证1000期指**: +1.20% → **多** (Score: 1.0)
- **维度综合**: **多** (Score: 1.0)

#### 二、资金面
- **融资融券**: 余额增加 → **多** (Score: 1.0)
- **北向资金**: 净流入10亿 → **多** (Score: 1.0)
- **行业资金流**: 总净流入50亿 → **多** (Score: 1.0)
- **龙虎榜机构**: 净买入12亿 → **多** (Score: 1.0)
- **维度综合**: **多** (Score: 1.0)

#### 三、情绪面
- **涨停板环境**: 涨停家数85，最高板5板 → **多** (Score: 1.0)
- **涨停溢价**: 溢价率5% → **多** (Score: 1.0)
- **炸板率**: 15% → **多** (Score: 1.0)
- **维度综合**: **多** (Score: 1.0)

#### 四、外围市场
- **新加坡A50**: +0.30% → **多** (Score: 0.1)
- **纳斯达克**: +0.50% → **多** (Score: 0.1)
- **美元指数**: -0.20% → **多** (Score: 0.1)
- **中概ETF**: +0.40% → **多** (Score: 0.1)
- **维度综合**: **多** (Score: 0.1)

#### 五、综合判断
- **综合评分**: 0.85
- **市场信号**: **多**
- **信号强度**: **强**

#### 六、操作建议
- **短期策略**: 激进
- **仓位建议**: 高
- **关注方向**: 科技、新能源、医药

> ⚠️ **免责声明**：以上分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。数据来源于公开市场，可能存在延迟。

## 注意事项

- 数据来自 akshare 和东方财富公开接口，盘中为实时数据，收盘后为收盘数据
- 部分指标（如A50期指、新加坡A50、美元指数、中概ETF）使用模拟数据，实际使用时需要替换为真实数据源
- 若 API 返回错误，系统会返回中性信号并记录错误信息
- 分析结果基于历史数据，不保证未来走势
- 权重设置可根据市场情况进行调整

## 技术实现

### 项目结构

```
market_sentiment_analysis/
├── astock_metrics/       # 数据采集层
│   ├── data/            # 数据采集模块
│   │   ├── futures.py   # 期货数据
│   │   ├── margin.py    # 融资融券数据
│   │   ├── northbound.py # 北向资金数据
│   │   ├── industry_flow.py # 行业资金流数据
│   │   ├── lhb.py       # 龙虎榜数据
│   │   ├── limitup.py    # 涨停板数据
│   │   └── external.py   # 外围市场数据
├── metrics/             # 指标评分层
│   ├── index_metrics.py    # 指数指标评分
│   ├── fund_metrics.py     # 资金指标评分
│   ├── sentiment_metrics.py # 情绪指标评分
│   └── external_metrics.py  # 外部指标评分
├── decision/            # 综合决策层
│   └── market_direction.py # 市场方向分析
├── scripts/             # 脚本
│   └── analyze_market_sentiment.py # 分析脚本
└── market_sentiment_analysis.md # 分析文档
```

### 核心功能

1. **数据采集**：从各个数据源获取原始数据
2. **指标计算**：计算每个指标的多空信号和评分
3. **维度评分**：计算各维度的综合评分
4. **市场分析**：基于所有指标生成市场情绪分析报告
5. **操作建议**：根据分析结果给出操作建议

### 使用方法

```python
# 导入模块
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
result = analyze_market_direction(all_metrics)
print(f"市场方向: {result['signal']}")
print(f"综合评分: {result['score']}")
```