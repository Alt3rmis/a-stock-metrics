"""
涨停板数据获取模块

数据源: akshare 涨停池数据
多空判断: 涨停环境评分 > 0 → 多, < 0 → 空

使用示例:
    from astock_metrics.limitup import get_limitup

    result = get_limitup(date="20250310")
    print(result)  # {"signal": "多", "total_zt": 85, ...}
"""

import akshare as ak
import pandas as pd
from typing import Dict, Any


def _find_col(df: pd.DataFrame, keyword: str) -> str:
    """在列名中模糊搜索包含 keyword 的列"""
    for col in df.columns:
        if keyword in col:
            return col
    raise ValueError(f"未找到包含 '{keyword}' 的列名, 实际列名: {list(df.columns)}")


def analyze_limitup_structure(date: str, top_n_industry: int = 5) -> Dict[str, Any]:
    """
    涨停板结构分析

    Args:
        date: 日期 (YYYYMMDD)
        top_n_industry: 返回TOP N行业

    Returns:
        Dict: 涨停结构数据
    """
    df_zt = ak.stock_zt_pool_em(date=date)
    if df_zt.empty:
        raise ValueError(f"{date} 无涨停数据")

    lb_col = _find_col(df_zt, "连板")
    ind_col = _find_col(df_zt, "所属行业")

    df_zt[lb_col] = pd.to_numeric(df_zt[lb_col], errors="coerce").fillna(1)

    total_zt = len(df_zt)
    max_lb = int(df_zt[lb_col].max())
    lb_dist = df_zt[lb_col].value_counts().sort_index()

    industry_top = df_zt[ind_col].value_counts().head(top_n_industry)

    return {
        "date": date,
        "total_zt": int(total_zt),
        "max_lb": max_lb,
        "lb_dist": lb_dist,
        "industry_top": industry_top,
        "df": df_zt,
    }


def analyze_limitup_break(date: str) -> Dict[str, Any]:
    """
    炸板股池分析

    Args:
        date: 日期 (YYYYMMDD)

    Returns:
        Dict: 炸板数据
    """
    df_zb = ak.stock_zt_pool_zbgc_em(date=date)
    if df_zb.empty:
        return {
            "date": date,
            "total_zb": 0,
            "industry_dist": pd.Series(dtype=int),
            "df": df_zb,
        }

    ind_col = _find_col(df_zb, "所属行业")

    total_zb = len(df_zb)
    industry_dist = df_zb[ind_col].value_counts()

    return {
        "date": date,
        "total_zb": int(total_zb),
        "industry_dist": industry_dist,
        "df": df_zb,
    }


def analyze_tier_structure(lb_dist: pd.Series, max_lb: int) -> Dict[str, Any]:
    """
    分析涨停梯队结构完整度

    Args:
        lb_dist: 连板分布
        max_lb: 最高板

    Returns:
        Dict: 梯队结构分析
    """
    tiers = {i: lb_dist.get(i, 0) for i in range(1, max_lb + 1)}

    active_tiers = [i for i, count in tiers.items() if count > 0]
    tier_count = len(active_tiers)

    if tier_count >= 4:
        tier_quality = "梯队结构完整，接力顺畅"
    elif tier_count >= 2:
        tier_quality = "梯队结构部分完整，存在接力机会"
    else:
        tier_quality = "梯队结构单一，接力困难"

    return {
        "tiers": tiers,
        "active_tiers": active_tiers,
        "tier_count": tier_count,
        "tier_quality": tier_quality,
        "dominant_tier": active_tiers[0] if active_tiers else 0
    }


def analyze_sector_graduation(struct: Dict, breaks: Dict | None) -> Dict[str, Any]:
    """
    分析板块是否出现"毕业照"迹象

    Args:
        struct: 涨停结构数据
        breaks: 炸板数据

    Returns:
        Dict: 毕业照分析
    """
    total_zt = struct["total_zt"]
    max_lb = struct["max_lb"]
    industry_top = struct.get("industry_top", pd.Series())

    total_zb = 0
    if breaks is not None:
        total_zb = breaks["total_zb"]

    break_ratio = total_zb / (total_zt + 1e-6)

    if not industry_top.empty:
        top5_concentration = industry_top.head(5).sum() / total_zt
    else:
        top5_concentration = 0

    graduation_signals = []
    graduation_score = 0

    if max_lb <= 2:
        graduation_signals.append("最高板<=2，高标严重断板")
        graduation_score += 2
    elif max_lb == 3:
        graduation_signals.append("最高板=3，高标承压")
        graduation_score += 1

    if total_zt < 30:
        graduation_signals.append("涨停家数<30，情绪极弱")
        graduation_score += 2
    elif total_zt < 50:
        graduation_signals.append("涨停家数<50，情绪降温")
        graduation_score += 1

    if break_ratio > 0.5:
        graduation_signals.append(f"炸板率{break_ratio:.1%}极高")
        graduation_score += 2
    elif break_ratio > 0.35:
        graduation_signals.append(f"炸板率{break_ratio:.1%}偏高")
        graduation_score += 1

    if top5_concentration < 0.35:
        graduation_signals.append(f"行业集中度{top5_concentration:.1%}较低")
        graduation_score += 1

    if graduation_score >= 4:
        graduation_status = "明显毕业照"
    elif graduation_score >= 2:
        graduation_status = "疑似毕业照"
    else:
        graduation_status = "梯队正常"

    return {
        "graduation_status": graduation_status,
        "graduation_score": graduation_score,
        "graduation_signals": graduation_signals,
        "break_ratio": break_ratio,
        "top5_concentration": top5_concentration
    }


def score_limitup_env(struct: Dict, breaks: Dict | None) -> tuple:
    """
    根据涨停结构+炸板情况评分

    Args:
        struct: 涨停结构数据
        breaks: 炸板数据

    Returns:
        tuple: (描述, 分值) 分值: +1强/0中性/-1弱
    """
    total_zt = struct["total_zt"]
    max_lb = struct["max_lb"]

    total_zb = 0
    if breaks is not None:
        total_zb = breaks["total_zb"]

    break_ratio = total_zb / (total_zt + 1e-6)

    if max_lb >= 4 and total_zt >= 80 and break_ratio < 0.35:
        return "涨停结构强，适合接力", +1

    if max_lb <= 2 or total_zt <= 30 or break_ratio > 0.5:
        return "涨停结构弱，集中毕业照/上板失败多", -1

    return "涨停结构一般，分歧/震荡", 0


def get_limitup(date: str, top_n_industry: int = 5) -> Dict[str, Any]:
    """
    获取涨停板数据（统一接口）

    Args:
        date: 日期 (YYYYMMDD)
        top_n_industry: 行业TOP N

    Returns:
        Dict: 标准格式的指标结果
    """
    try:
        struct = analyze_limitup_structure(date=date, top_n_industry=top_n_industry)
        breaks = analyze_limitup_break(date=date)
        env_desc, env_score = score_limitup_env(struct, breaks)
        tier_analysis = analyze_tier_structure(struct["lb_dist"], struct["max_lb"])
        graduation_analysis = analyze_sector_graduation(struct, breaks)

        if env_score > 0:
            signal = "多"
            signal_value = 1
        elif env_score < 0:
            signal = "空"
            signal_value = -1
        else:
            signal = "中性"
            signal_value = 0
        
        weight = 1
        score = signal_value * weight

        return {
            "metric_id": "limitup",
            "name": "涨停板环境",
            "signal": signal,
            "signal_value": signal_value,
            "weight": weight,
            "score": score,
            "detail": {
                "date": date,
                "env_desc": env_desc,
                "total_zt": struct["total_zt"],
                "max_lb": struct["max_lb"],
                "total_zb": breaks["total_zb"],
                "break_ratio": graduation_analysis["break_ratio"],
                "tier_quality": tier_analysis["tier_quality"],
                "graduation_status": graduation_analysis["graduation_status"]
            },
            "error": None
        }
    except Exception as e:
        return {
            "metric_id": "limitup",
            "name": "涨停板环境",
            "signal": "中性",
            "signal_value": 0,
            "weight": 1,
            "score": 0,
            "detail": {},
            "error": str(e)
        }

def get_limitup_premium(date: str) -> Dict[str, Any]:
    """
    获取涨停溢价数据（统一接口）

    Args:
        date: 日期 (YYYYMMDD)

    Returns:
        Dict: 标准格式的指标结果
    """
    try:
        # 这里实现涨停溢价计算逻辑
        # 模拟数据
        premium = 0.05
        if premium > 0.03:
            signal = "多"
            signal_value = 1
        elif premium < -0.03:
            signal = "空"
            signal_value = -1
        else:
            signal = "中性"
            signal_value = 0
        
        weight = 1
        score = signal_value * weight

        return {
            "metric_id": "limitup_premium",
            "name": "涨停溢价",
            "signal": signal,
            "signal_value": signal_value,
            "weight": weight,
            "score": score,
            "detail": {
                "date": date,
                "premium": premium
            },
            "error": None
        }
    except Exception as e:
        return {
            "metric_id": "limitup_premium",
            "name": "涨停溢价",
            "signal": "中性",
            "signal_value": 0,
            "weight": 1,
            "score": 0,
            "detail": {},
            "error": str(e)
        }

def get_break_rate(date: str) -> Dict[str, Any]:
    """
    获取炸板率数据（统一接口）

    Args:
        date: 日期 (YYYYMMDD)

    Returns:
        Dict: 标准格式的指标结果
    """
    try:
        struct = analyze_limitup_structure(date=date)
        breaks = analyze_limitup_break(date=date)
        total_zt = struct["total_zt"]
        total_zb = breaks["total_zb"]
        break_rate = total_zb / (total_zt + 1e-6)
        
        if break_rate < 0.3:
            signal = "多"
            signal_value = 1
        elif break_rate > 0.5:
            signal = "空"
            signal_value = -1
        else:
            signal = "中性"
            signal_value = 0
        
        weight = 1
        score = signal_value * weight

        return {
            "metric_id": "break_rate",
            "name": "炸板率",
            "signal": signal,
            "signal_value": signal_value,
            "weight": weight,
            "score": score,
            "detail": {
                "date": date,
                "total_zt": total_zt,
                "total_zb": total_zb,
                "break_rate": break_rate
            },
            "error": None
        }
    except Exception as e:
        return {
            "metric_id": "break_rate",
            "name": "炸板率",
            "signal": "中性",
            "signal_value": 0,
            "weight": 1,
            "score": 0,
            "detail": {},
            "error": str(e)
        }


if __name__ == "__main__":
    result = get_limitup(date="20250123")
    print(f"涨停家数: {result.get('struct', {}).get('total_zt', 0)}")
    print(f"最高板: {result.get('struct', {}).get('max_lb', 0)}板")
    print(f"环境: {result.get('env_desc', '-')}")
