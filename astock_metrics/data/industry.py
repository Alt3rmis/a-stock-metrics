"""
行业资金流数据获取模块

数据源: akshare 同花顺-行业资金流3日排行
多空判断: 无直接信号，提供资金流入/流出排行

使用示例:
    from astock_metrics.industry import get_industry_flow

    result = get_industry_flow(top_n=5)
    print(result)  # {"top_in": [...], "top_out": [...]}
"""

import akshare as ak
from typing import Dict, Any


def fetch_industry_fund_flow_3d(top_n: int = 5):
    """
    获取同花顺-行业资金流3日排行

    Args:
        top_n: 返回TOP N

    Returns:
        tuple: (净流入TopN, 净流出TopN)
    """
    df = ak.stock_fund_flow_industry(symbol="3日排行")

    top_in = (
        df.sort_values("净额", ascending=False)
        .head(top_n)
        .loc[:, ["行业", "净额", "流入资金", "流出资金", "阶段涨跌幅"]]
    )

    top_out = (
        df.sort_values("净额", ascending=True)
        .head(top_n)
        .loc[:, ["行业", "净额", "流入资金", "流出资金", "阶段涨跌幅"]]
    )

    return top_in, top_out


def get_industry_flow(top_n: int = 5) -> Dict[str, Any]:
    """
    获取行业资金流数据（统一接口）

    Args:
        top_n: 返回TOP N

    Returns:
        Dict: 包含流入流出排行
    """
    try:
        top_in, top_out = fetch_industry_fund_flow_3d(top_n=top_n)

        return {
            "metric_id": "industry_flow",
            "name": "行业资金流",
            "name_en": "Industry Fund Flow",
            "signal": "中性",
            "score": 0,
            "top_in": top_in.to_dict("records") if top_in is not None else [],
            "top_out": top_out.to_dict("records") if top_out is not None else [],
            "error": None
        }
    except Exception as e:
        return {
            "metric_id": "industry_flow",
            "name": "行业资金流",
            "signal": "中性",
            "score": 0,
            "error": str(e)
        }


if __name__ == "__main__":
    result = get_industry_flow(top_n=5)
    print("净流入TOP5:")
    for item in result.get("top_in", []):
        print(f"  {item['行业']}: {item['净额']:+.2f}亿")

    print("\n净流出TOP5:")
    for item in result.get("top_out", []):
        print(f"  {item['行业']}: {item['净额']:+.2f}亿")
