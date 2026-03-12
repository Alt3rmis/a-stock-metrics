"""
融资融券数据获取模块

数据源: akshare (沪深两市融资融券余额合计)
多空判断: 近N日余额变化 > 0 → 多, < 0 → 空

使用示例:
    from astock_metrics.margin import get_margin

    result = get_margin(days=3)
    print(result)  # {"signal": "多", "delta": 123456, ...}
"""

import akshare as ak
import pandas as pd
from typing import Dict, Any


def _find_total_margin_col(df: pd.DataFrame) -> str:
    """
    在 DataFrame 列名中寻找包含"融资融券余额"的列名
    """
    for col in df.columns:
        if "融资融券余额" in col:
            return col
    raise ValueError(f"未找到包含 '融资融券余额' 的列名，实际列名: {list(df.columns)}")


def fetch_total_margin_change(days: int = 3):
    """
    获取沪深两市融资融券余额合计，并计算最近 N 日的变化

    Args:
        days: 计算变化的天数

    Returns:
        tuple: (最近日期, 起始余额, 结束余额, 变化额)
    """
    sz = ak.macro_china_market_margin_sz()
    sh = ak.macro_china_market_margin_sh()

    sz_col = _find_total_margin_col(sz)
    sh_col = _find_total_margin_col(sh)

    sz["日期"] = pd.to_datetime(sz["日期"])
    sh["日期"] = pd.to_datetime(sh["日期"])

    sz = sz.set_index("日期")
    sh = sh.set_index("日期")

    merged = pd.DataFrame({
        "sz": pd.to_numeric(sz[sz_col], errors="coerce"),
        "sh": pd.to_numeric(sh[sh_col], errors="coerce"),
    }).dropna()

    merged["total_margin"] = merged["sz"] + merged["sh"]

    recent = merged.tail(days + 1)
    if recent.shape[0] < 2:
        raise ValueError("融资融券数据不足，无法计算变化")

    start = recent["total_margin"].iloc[0]
    end = recent["total_margin"].iloc[-1]
    delta = end - start
    latest_date = recent.index[-1].date()

    return latest_date, start, end, delta


def judge_margin_signal(delta: float, threshold_ratio: float = 0.005, base: float | None = None) -> str:
    """
    根据融资融券余额变化判断多空

    Args:
        delta: 变化额
        threshold_ratio: 判断阈值比例
        base: 基准余额（用于计算比例）

    Returns:
        str: 多空信号描述
    """
    if base is not None:
        ratio = delta / base
        if ratio > threshold_ratio:
            return "融资余额明显增加 → 偏多"
        elif ratio < -threshold_ratio:
            return "融资余额明显减少 → 偏空"
        else:
            return "变化不大 → 中性"
    else:
        if delta > 0:
            return "融资余额增加 → 偏多"
        elif delta < 0:
            return "融资余额减少 → 偏空"
        else:
            return "中性"


def get_margin(days: int = 3) -> Dict[str, Any]:
    """
    获取融资融券数据（统一接口）

    Args:
        days: 计算变化的天数

    Returns:
        Dict: 包含信号、原始数据等信息
            - latest_date: 最新日期
            - start: 起始余额
            - end: 当前余额
            - delta: 变化额
            - days: 天数
            - signal: 信号 ("多"/"空"/"中性")
            - signal_desc: 信号描述
            - score: 分值 (+1/-1/0)
    """
    try:
        latest_date, start, end, delta = fetch_total_margin_change(days=days)
        signal_desc = judge_margin_signal(delta, base=start)

        if delta > 0:
            signal = "多"
            score = 1
        elif delta < 0:
            signal = "空"
            score = -1
        else:
            signal = "中性"
            score = 0

        return {
            "metric_id": "margin",
            "name": "融资融券",
            "latest_date": str(latest_date),
            "start": start,
            "end": end,
            "delta": delta,
            "days": days,
            "signal": signal,
            "signal_desc": signal_desc,
            "score": score,
            "error": None
        }
    except Exception as e:
        return {
            "metric_id": "margin",
            "name": "融资融券",
            "signal": "中性",
            "score": 0,
            "error": str(e)
        }


if __name__ == "__main__":
    result = get_margin(days=3)
    print(f"日期: {result['latest_date']}")
    print(f"余额变化: {result['delta']:+,.0f}")
    print(f"信号: {result['signal_desc']}")
