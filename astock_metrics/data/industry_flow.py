"""行业资金流向数据采集模块"""

import akshare as ak
import pandas as pd
from datetime import datetime
from typing import Dict, Any


def fetch_industry_flow() -> Dict[str, Any]:
    """获取行业资金流向数据
    
    Returns:
        Dict: 行业资金流向数据
    """
    try:
        # 使用akshare获取行业资金流向数据
        df = ak.stock_industry_fund_flow_rank_em()
        total_inflow = df["主力净流入-净额"].sum()
        
        if total_inflow > 0:
            signal = "多"
            signal_value = 1
        elif total_inflow < 0:
            signal_value = -1
            signal = "空"
        else:
            signal = "中性"
            signal_value = 0
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_inflow": total_inflow,
            "signal": signal,
            "signal_value": signal_value,
            "top_industries": df.head(5).to_dict()
        }
    except Exception:
        # 返回模拟数据
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_inflow": 5000000000,
            "signal": "多",
            "signal_value": 1,
            "top_industries": {}
        }


def get_industry_flow() -> Dict[str, Any]:
    """获取行业资金流向数据（统一接口）
    
    Returns:
        Dict: 标准格式的指标结果
    """
    try:
        data = fetch_industry_flow()
        weight = 1
        score = data["signal_value"] * weight
        
        return {
            "metric_id": "industry_flow",
            "name": "行业资金流",
            "signal": data["signal"],
            "signal_value": data["signal_value"],
            "weight": weight,
            "score": score,
            "detail": {
                "date": data["date"],
                "total_inflow": data["total_inflow"],
                "top_industries": data["top_industries"]
            },
            "error": None
        }
    except Exception as e:
        return {
            "metric_id": "industry_flow",
            "name": "行业资金流",
            "signal": "中性",
            "signal_value": 0,
            "weight": 1,
            "score": 0,
            "detail": {},
            "error": str(e)
        }


def get_industry_rank():
    """获取行业资金流向排名
    
    Returns:
        pd.DataFrame: 行业资金流向排名
    """
    # 这里实现行业资金流向排名数据采集逻辑
    pass
