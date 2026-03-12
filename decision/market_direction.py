"""市场方向综合决策模块"""

import pandas as pd
import numpy as np
from typing import Dict, List


def analyze_market_direction(metrics: List[Dict]) -> Dict:
    """分析市场方向
    
    Args:
        metrics: 所有指标列表
    
    Returns:
        dict: 市场方向分析结果
    """
    if not metrics:
        return {
            "metric_id": "market_direction",
            "name": "市场方向综合",
            "signal": "中性",
            "signal_value": 0,
            "weight": 1,
            "score": 0,
            "detail": {},
            "error": "No metrics provided"
        }
    
    # 计算所有指标的加权平均分
    total_score = sum(m["score"] for m in metrics if m.get("error") is None)
    valid_count = sum(1 for m in metrics if m.get("error") is None)
    
    if valid_count == 0:
        return {
            "metric_id": "market_direction",
            "name": "市场方向综合",
            "signal": "中性",
            "signal_value": 0,
            "weight": 1,
            "score": 0,
            "detail": {},
            "error": "No valid metrics"
        }
    
    avg_score = total_score / valid_count
    
    if avg_score > 0.5:
        signal = "多"
        signal_value = 1
    elif avg_score < -0.5:
        signal = "空"
        signal_value = -1
    else:
        signal = "中性"
        signal_value = 0
    
    score = signal_value * 1  # 权重为1
    
    # 按类型分组统计
    type_stats = {}
    for metric in metrics:
        if metric.get("error") is None:
            # 这里简化处理，实际应该根据metric_id判断类型
            metric_type = "其他"
            if metric["metric_id"] in ["a50", "if_main", "im_main"]:
                metric_type = "指数预期"
            elif metric["metric_id"] in ["margin", "northbound", "industry_flow", "lhb"]:
                metric_type = "资金"
            elif metric["metric_id"] in ["limitup", "limitup_premium", "break_rate"]:
                metric_type = "情绪"
            elif metric["metric_id"] in ["singapore_a50", "nasdaq", "usd_index", "china_etf"]:
                metric_type = "外围"
            
            if metric_type not in type_stats:
                type_stats[metric_type] = {
                    "count": 0,
                    "total_score": 0,
                    "signals": []
                }
            type_stats[metric_type]["count"] += 1
            type_stats[metric_type]["total_score"] += metric["score"]
            type_stats[metric_type]["signals"].append(metric["signal"])
    
    # 计算各类型的平均分数
    for metric_type, stats in type_stats.items():
        stats["avg_score"] = stats["total_score"] / stats["count"]
    
    return {
        "metric_id": "market_direction",
        "name": "市场方向综合",
        "signal": signal,
        "signal_value": signal_value,
        "weight": 1,
        "score": score,
        "detail": {
            "avg_score": avg_score,
            "valid_count": valid_count,
            "metrics_count": len(metrics),
            "type_stats": type_stats
        },
        "error": None
    }


def get_market_signal(metrics: List[Dict]) -> str:
    """获取市场信号
    
    Args:
        metrics: 所有指标列表
    
    Returns:
        str: 市场信号
    """
    result = analyze_market_direction(metrics)
    return result["signal"]
