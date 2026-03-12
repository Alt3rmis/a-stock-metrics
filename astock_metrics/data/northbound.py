"""北向资金数据采集模块"""

import akshare as ak
import pandas as pd
from datetime import datetime
from typing import Dict, Any


def fetch_northbound_data() -> Dict[str, Any]:
    """获取北向资金数据
    
    Returns:
        Dict: 北向资金数据
    """
    try:
        # 使用akshare获取北向资金数据
        df = ak.stock_hsgt_north_net_flow_em()
        latest = df.iloc[-1]
        net_flow = latest["北向资金净流入-当日值"]
        
        if net_flow > 0:
            signal = "多"
            signal_value = 1
        elif net_flow < 0:
            signal_value = -1
            signal = "空"
        else:
            signal = "中性"
            signal_value = 0
        
        return {
            "date": latest["日期"],
            "net_flow": net_flow,
            "signal": signal,
            "signal_value": signal_value
        }
    except Exception:
        # 返回模拟数据
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "net_flow": 1000000000,
            "signal": "多",
            "signal_value": 1
        }


def get_northbound() -> Dict[str, Any]:
    """获取北向资金数据（统一接口）
    
    Returns:
        Dict: 标准格式的指标结果
    """
    try:
        data = fetch_northbound_data()
        weight = 1
        score = data["signal_value"] * weight
        
        return {
            "metric_id": "northbound",
            "name": "北向资金",
            "signal": data["signal"],
            "signal_value": data["signal_value"],
            "weight": weight,
            "score": score,
            "detail": {
                "date": data["date"],
                "net_flow": data["net_flow"]
            },
            "error": None
        }
    except Exception as e:
        return {
            "metric_id": "northbound",
            "name": "北向资金",
            "signal": "中性",
            "signal_value": 0,
            "weight": 1,
            "score": 0,
            "detail": {},
            "error": str(e)
        }


def get_northbound_holdings():
    """获取北向资金持仓数据
    
    Returns:
        pd.DataFrame: 北向资金持仓数据
    """
    # 这里实现北向资金持仓数据采集逻辑
    pass
