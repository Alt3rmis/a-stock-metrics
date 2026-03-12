"""
龙虎榜机构资金数据获取模块

数据源: 东方财富网-龙虎榜单-机构买卖每日统计
多空判断: 机构净买入 > 0 → 多, < 0 → 空

使用示例:
    from astock_metrics.lhb import get_lhb

    result = get_lhb(date="20250310")
    print(result)  # {"signal": "多", "total_net": 123456789, ...}
"""

import akshare as ak
import pandas as pd
import requests
from akshare.utils.tqdm import get_tqdm
import secrets
import string
from datetime import datetime
from typing import Tuple, Dict, Any
from functools import lru_cache


def _generate_nid() -> Tuple[str, int]:
    """
    生成 nid 和创建时间（毫秒时间戳）
    """
    alphabet = string.ascii_lowercase + string.digits
    nid = ''.join(secrets.choice(alphabet) for _ in range(32))
    create_time_ms = int(datetime.now().timestamp() * 1000)
    return nid, create_time_ms


def _find_col(df: pd.DataFrame, keyword: str) -> str:
    """
    在列名中模糊搜索包含 keyword 的列
    """
    for col in df.columns:
        if keyword in col:
            return col
    raise ValueError(f"未找到包含 '{keyword}' 的列名，实际列名: {list(df.columns)}")


def stock_lhb_jgmmtj_em(
    start_date: str = "20240417", end_date: str = "20240430"
) -> pd.DataFrame:
    """
    东方财富网-数据中心-龙虎榜单-机构买卖每日统计

    Args:
        start_date: 开始日期 (YYYYMMDD)
        end_date: 结束日期 (YYYYMMDD)

    Returns:
        pd.DataFrame: 机构买卖每日统计
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    nid, create_time_ms = _generate_nid()
    headers = {
        "cookie": f"nid18={nid}; nid18_create_time={create_time_ms};",
        "host": "datacenter-web.eastmoney.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://data.eastmoney.com/stock/jgmmtj.html"
    }
    params = {
        "sortColumns": "NET_BUY_AMT,TRADE_DATE,SECURITY_CODE",
        "sortTypes": "-1,-1,1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_ORGANIZATION_TRADE_DETAILS",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"(TRADE_DATE>='{start_date}')(TRADE_DATE<='{end_date}')",
    }
    r = requests.get(url, params=params, headers=headers, timeout=10)

    if r.status_code != 200:
        raise ValueError(f"API请求失败，状态码: {r.status_code}")

    data_json = r.json()

    if "result" not in data_json or data_json["result"] is None:
        raise ValueError(f"API返回数据为空")

    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params["pageNumber"] = page
        r = requests.get(url, params=params, headers=headers, timeout=10)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df["index"] = big_df.index + 1
    big_df.columns = [
        "序号", "-", "名称", "代码", "上榜日期", "收盘价", "涨跌幅",
        "买方机构数", "卖方机构数", "机构买入总额", "机构卖出总额",
        "机构买入净额", "市场总成交额", "机构净买额占总成交额比",
        "换手率", "流通市值", "上榜原因", "-", "-", "-", "-", "-", "-", "-", "-", "-",
    ]
    big_df = big_df[
        ["序号", "代码", "名称", "收盘价", "涨跌幅", "买方机构数", "卖方机构数",
         "机构买入总额", "机构卖出总额", "机构买入净额", "市场总成交额",
         "机构净买额占总成交额比", "换手率", "流通市值", "上榜原因", "上榜日期"]
    ]
    big_df["上榜日期"] = pd.to_datetime(big_df["上榜日期"], errors="coerce").dt.date
    big_df["收盘价"] = pd.to_numeric(big_df["收盘价"], errors="coerce")
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"], errors="coerce")
    big_df["买方机构数"] = pd.to_numeric(big_df["买方机构数"], errors="coerce")
    big_df["卖方机构数"] = pd.to_numeric(big_df["卖方机构数"], errors="coerce")
    big_df["机构买入总额"] = pd.to_numeric(big_df["机构买入总额"], errors="coerce")
    big_df["机构卖出总额"] = pd.to_numeric(big_df["机构卖出总额"], errors="coerce")
    big_df["机构买入净额"] = pd.to_numeric(big_df["机构买入净额"], errors="coerce")
    big_df["市场总成交额"] = pd.to_numeric(big_df["市场总成交额"], errors="coerce")
    big_df["机构净买额占总成交额比"] = pd.to_numeric(big_df["机构净买额占总成交额比"], errors="coerce")
    big_df["换手率"] = pd.to_numeric(big_df["换手率"], errors="coerce")
    big_df["流通市值"] = pd.to_numeric(big_df["流通市值"], errors="coerce")
    return big_df


def fetch_lhb_institution_flow(start_date: str, end_date: str | None = None):
    """
    获取龙虎榜机构买卖统计

    Args:
        start_date: 开始日期 (YYYYMMDD)
        end_date: 结束日期 (YYYYMMDD)，如果为None则取单日

    Returns:
        tuple: (明细DataFrame, 机构净买入总额)
    """
    if end_date is None:
        end_date = start_date

    df = stock_lhb_jgmmtj_em(start_date=start_date, end_date=end_date)

    if df.empty:
        raise ValueError("机构买卖每日统计返回空数据")

    try:
        net_col = _find_col(df, "净买")
    except ValueError:
        buy_col = _find_col(df, "买入")
        sell_col = _find_col(df, "卖出")
        df["机构净买额"] = pd.to_numeric(df[buy_col], errors="coerce") - pd.to_numeric(df[sell_col], errors="coerce")
        net_col = "机构净买额"

    df[net_col] = pd.to_numeric(df[net_col], errors="coerce")
    total_net = df[net_col].sum()

    return df, total_net


@lru_cache(maxsize=512)
def _get_stock_industry(code: str) -> str | None:
    """获取股票所属行业"""
    try:
        info_df = ak.stock_individual_info_em(symbol=code)
    except Exception:
        return None

    if info_df is None or info_df.empty:
        return None

    row = info_df[info_df["item"].str.contains("所属行业", na=False)]
    if row.empty:
        return None

    return str(row["value"].iloc[0]).strip() or None


def analyze_lhb_hot_industries(df: pd.DataFrame, top_n: int = 5):
    """
    分析龙虎榜热门行业

    Args:
        df: 龙虎榜明细DataFrame
        top_n: 返回TOP N

    Returns:
        tuple: (热门做多行业, 机构净卖出行业)
    """
    if df.empty:
        raise ValueError("空的龙虎榜数据")

    if "机构买入净额" not in df.columns:
        net_col = _find_col(df, "净买")
        df["机构买入净额"] = pd.to_numeric(df[net_col], errors="coerce")
    else:
        df["机构买入净额"] = pd.to_numeric(df["机构买入净额"], errors="coerce")

    df = df.copy()
    df["行业"] = df["代码"].astype(str).str.zfill(6).map(_get_stock_industry)

    non_null_industry = df["行业"].notna().sum()

    if non_null_industry > 0:
        grouped = (
            df[~df["行业"].isna()]
            .groupby("行业")["机构买入净额"]
            .agg(上榜次数="count", 净买入总额="sum")
            .sort_values(["净买入总额", "上榜次数"], ascending=[False, False])
        )
    else:
        grouped = (
            df.groupby("名称")["机构买入净额"]
            .agg(上榜次数="count", 净买入总额="sum")
            .sort_values(["净买入总额", "上榜次数"], ascending=[False, False])
        )

    hot_buy = grouped[grouped["净买入总额"] > 0].head(top_n)
    hot_sell = (
        grouped[grouped["净买入总额"] < 0]
        .sort_values("净买入总额", ascending=True)
        .head(top_n)
    )

    return hot_buy, hot_sell


def judge_lhb_institution_signal(total_net: float, threshold: float = 0) -> str:
    """
    根据机构净买入判断多空

    Args:
        total_net: 机构净买入总额
        threshold: 判断阈值

    Returns:
        str: 多空信号描述
    """
    if total_net > threshold:
        return "机构整体净买入 → 偏多"
    elif total_net < -threshold:
        return "机构整体净卖出 → 偏空"
    else:
        return "机构买卖接近均衡 → 中性"


def get_lhb(date: str, top_n: int = 5) -> Dict[str, Any]:
    """
    获取龙虎榜数据（统一接口）

    Args:
        date: 日期 (YYYYMMDD)
        top_n: 热门行业TOP N

    Returns:
        Dict: 包含信号、原始数据等信息
    """
    try:
        df_lhb, total_net = fetch_lhb_institution_flow(start_date=date)
        signal_desc = judge_lhb_institution_signal(total_net)

        if total_net > 0:
            signal = "多"
            score = 1
        elif total_net < 0:
            signal = "空"
            score = -1
        else:
            signal = "中性"
            score = 0

        hot_buy = None
        hot_sell = None
        try:
            hot_buy, hot_sell = analyze_lhb_hot_industries(df_lhb, top_n=top_n)
        except Exception:
            pass

        return {
            "metric_id": "lhb",
            "name": "龙虎榜",
            "name_en": "Long-Hu Bang",
            "date": date,
            "total_net": total_net,
            "record_count": len(df_lhb),
            "signal": signal,
            "signal_desc": signal_desc,
            "score": score,
            "hot_buy": hot_buy.to_dict() if hot_buy is not None else None,
            "hot_sell": hot_sell.to_dict() if hot_sell is not None else None,
            "error": None
        }
    except Exception as e:
        return {
            "metric_id": "lhb",
            "name": "龙虎榜",
            "date": date,
            "signal": "中性",
            "score": 0,
            "error": str(e)
        }


if __name__ == "__main__":
    result = get_lhb(date="20250123")
    print(f"机构净买入: {result.get('total_net', 0):,.0f}")
    print(f"信号: {result.get('signal_desc', '-')}")
