"""
A股市场数据指标获取包

提供原子化的数据获取接口，每个指标可独立调用。

使用示例:
    from astock_metrics import (
        get_margin,
        get_futures_if,
        get_futures_im,
        get_lhb,
        get_limitup,
        get_industry_flow
    )

    # 获取融资融券数据
    result = get_margin(days=3)

    # 获取沪深300期货信号
    result = get_futures_if()

    # 获取涨停板数据
    struct = get_limitup(date="20250310")
"""

from astock_metrics.margin import (
    fetch_total_margin_change,
    judge_margin_signal,
    get_margin
)

from astock_metrics.futures import (
    fetch_if_main,
    fetch_im_main,
    get_futures_if,
    get_futures_im
)

from astock_metrics.lhb import (
    fetch_lhb_institution_flow,
    judge_lhb_institution_signal,
    analyze_lhb_hot_industries,
    get_lhb
)

from astock_metrics.limitup import (
    analyze_limitup_structure,
    analyze_limitup_break,
    analyze_tier_structure,
    analyze_sector_graduation,
    score_limitup_env,
    get_limitup
)

from astock_metrics.industry import (
    fetch_industry_fund_flow_3d,
    get_industry_flow
)

__version__ = "0.1.0"
__all__ = [
    "fetch_total_margin_change",
    "judge_margin_signal",
    "get_margin",
    "fetch_if_main",
    "fetch_im_main",
    "get_futures_if",
    "get_futures_im",
    "fetch_lhb_institution_flow",
    "judge_lhb_institution_signal",
    "analyze_lhb_hot_industries",
    "get_lhb",
    "analyze_limitup_structure",
    "analyze_limitup_break",
    "analyze_tier_structure",
    "analyze_sector_graduation",
    "score_limitup_env",
    "get_limitup",
    "fetch_industry_fund_flow_3d",
    "get_industry_flow",
]
