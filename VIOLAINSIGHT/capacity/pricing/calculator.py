from .constants import MONTHLY_FEE, INITIAL_ANALYSIS


def calc_monthly(plan: str) -> int:
    """内部用の素の計算"""
    return MONTHLY_FEE.get(plan, 30000)


def calc_initial(version: str) -> int:
    """内部用の素の計算"""
    return INITIAL_ANALYSIS.get(version, 150000)


# === views.py から呼ばれる公開API ===

def get_monthly_fee(plan: str) -> int:
    """プランに応じた月額フィーを返す"""
    return calc_monthly(plan)


def get_initial_analysis(version: str) -> int:
    """ライト/フルの初期分析料金を返す"""
    return calc_initial(version)
