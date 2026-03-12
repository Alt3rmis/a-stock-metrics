"""
股指期货数据获取模块

数据源: akshare (沪深300、中证1000期货)
多空判断: 涨跌幅 > 0 → 多, < 0 → 空

使用示例:
    from astock_metrics.futures import get_futures_if, get_futures_im

    result = get_futures_if()
    print(result)  # {"signal": "多", "pct_change": 0.85, ...}
"""

import akshare as ak
from typing import Dict, Any


def _pct_change(close: float, prev_close: float) -> float:
    """计算涨跌幅百分比"""
    return (close / prev_close - 1) * 100


def _judge_signal(pct: float, threshold: float = 0) -> tuple:
    """
    期货信号判断

    Args:
        pct: 涨跌幅
        threshold: 判断阈值

    Returns:
        tuple: (信号, 分值)
    """
    if pct > threshold:
        return "多", 1
    elif pct < -threshold:
        return "空", -1
    else:
        return "中性", 0


def fetch_if_main() -> Dict[str, Any]:
    """
    获取沪深300股指期货(IF)主力合约数据

    Returns:
        Dict: 包含日期、涨跌幅、信号等
    """
    df = ak.futures_main_sina(symbol="IF0")
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    latest_close = latest["收盘价"]
    prev_close = prev["收盘价"]
    pct = _pct_change(latest_close, prev_close)

    signal, score = _judge_signal(pct)

    return {
        "name": "沪深300 股指期货(IF)",
        "date": latest["日期"],
        "pct_change": round(pct, 2),
        "signal": signal,
        "score": score,
    }


def fetch_im_main() -> Dict[str, Any]:
    """
    获取中证1000股指期货(IM)主力合约数据

    Returns:
        Dict: 包含日期、涨跌幅、信号等
    """
    df = ak.futures_main_sina(symbol="IM0")
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    latest_close = latest["收盘价"]
    prev_close = prev["收盘价"]
    pct = _pct_change(latest_close, prev_close)

    signal, score = _judge_signal(pct)

    return {
        "name": "中证1000 股指期货(IM)",
        "date": latest["日期"],
        "pct_change": round(pct, 2),
        "signal": signal,
        "score": score,
    }


def get_futures_if() -> Dict[str, Any]:
    """
    获取沪深300期货数据（统一接口）

    Returns:
        Dict: 标准格式的指标结果
    """
    try:
        data = fetch_if_main()
        return {
            "metric_id": "if_main",
            "name": "沪深300股指期货",
            "name_en": "CSI 300 Futures",
            **data,
            "error": None
        }
    except Exception as e:
        return {
            "metric_id": "if_main",
            "name": "沪深300股指期货",
            "signal": "中性",
            "score": 0,
            "error": str(e)
        }


def get_futures_im() -> Dict[str, Any]:
    """
    获取中证1000期货数据（统一接口）

    Returns:
        Dict: 标准格式的指标结果
    """
    try:
        data = fetch_im_main()
        return {
            "metric_id": "im_main",
            "name": "中证1000股指期货",
            "name_en": "CSI 1000 Futures",
            **data,
            "error": None
        }
    except Exception as e:
        return {
            "metric_id": "im_main",
            "name": "中证1000股指期货",
            "signal": "中性",
            "score": 0,
            "error": str(e)
        }


if __name__ == "__main__":
    if_result = get_futures_if()
    im_result = get_futures_im()

    print(f"IF: {if_result['pct_change']:+.2f}% | {if_result['signal']}")
    print(f"IM: {im_result['pct_change']:+.2f}% | {im_result['signal']}")
