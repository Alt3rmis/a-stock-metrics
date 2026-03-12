"""情绪指标评分模块"""

import pandas as pd
import numpy as np
from typing import Dict, List


def calculate_sentiment_metrics(metrics: List[Dict]) -> Dict:
    """计算情绪指标评分
    
    Args:
        metrics: 情绪相关指标列表
    
    Returns:
        Dict: 情绪指标综合评分
    """
    if not metrics:
        return {
            "metric_id": "sentiment_metrics",
            "name": "情绪指标综合",
            "signal": "中性",
            "signal_value": 0,
            "weight": 1,
            "score": 0,
            "detail": {},
            "error": "No metrics provided"
        }
    
    # 计算加权平均分
    total_score = sum(m["score"] for m in metrics if m.get("error") is None)
    valid_count = sum(1 for m in metrics if m.get("error") is None)
    
    if valid_count == 0:
        return {
            "metric_id": "sentiment_metrics",
            "name": "情绪指标综合",
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
    
    return {
        "metric_id": "sentiment_metrics",
        "name": "情绪指标综合",
        "signal": signal,
        "signal_value": signal_value,
        "weight": 1,
        "score": score,
        "detail": {
            "avg_score": avg_score,
            "valid_count": valid_count,
            "metrics_count": len(metrics)
        },
        "error": None
    }


def get_sentiment_strength(metrics: List[Dict]) -> Dict:
    """获取情绪强度评分
    
    Args:
        metrics: 情绪相关指标列表
    
    Returns:
        Dict: 情绪强度评分
    """
    return calculate_sentiment_metrics(metrics)
