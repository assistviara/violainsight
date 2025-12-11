# capacity/forms.py
from django import forms


class CapacityForm(forms.Form):
    # ベース条件
    annual_hours = forms.FloatField(
        label="年間稼働時間（VIOLAに使える時間）",
        initial=600,
        min_value=1,
    )
    target_income = forms.IntegerField(
        label="目標年収（円）",
        initial=6000000,
        min_value=0,
    )

    # プランごとの1件あたり工数（年換算）
    plan1_hours = forms.FloatField(
        label="プラン1：体質診断 1件あたり（時間／年換算）",
        initial=12.5,
        min_value=0.1,
    )
    plan2_hours = forms.FloatField(
        label="プラン2：月次伴走 1件あたり（時間／年）",
        initial=49,
        min_value=0.1,
    )
    plan3_hours = forms.FloatField(
        label="プラン3：棚卸診断 1件あたり（時間／年）",
        initial=12,
        min_value=0.1,
    )

    # ★追加：月次フィーのランク
    MONTHLY_TIER_CHOICES = [
        ("small", "小規模向け：3万円 / 月"),
        ("medium", "中規模向け：4万円 / 月"),
        ("large", "大規模向け：5万円 / 月"),
    ]
    monthly_tier = forms.ChoiceField(
        label="月次伴走フィーのランク",
        choices=MONTHLY_TIER_CHOICES,
        initial="small",
    )

    # ★追加：初期分析プラン
    ANALYSIS_TIER_CHOICES = [
        ("light", "ライト版 初期分析：15万円 / 回"),
        ("full", "フル版 初期分析：30万円 / 回"),
    ]
    analysis_tier = forms.ChoiceField(
        label="初期分析プラン",
        choices=ANALYSIS_TIER_CHOICES,
        initial="light",
    )

    # 「今こうしようかな」と考えている件数（シミュレーション用）
    plan2_clients = forms.IntegerField(
        label="プラン2（月次伴走）の件数",
        initial=5,
        min_value=0,
    )
    plan1_cases = forms.IntegerField(
        label="プラン1（体質診断）の件数／年",
        initial=4,
        min_value=0,
    )
    plan3_cases = forms.IntegerField(
        label="プラン3（棚卸診断）の件数／年",
        initial=4,
        min_value=0,
    )

    # 単価（空欄なら自動計算・上書きしたい時だけ入力）
    plan1_price = forms.IntegerField(
        label="プラン1 単価（円／回）※空欄ならプラン選択から自動計算",
        required=False,
        min_value=0,
    )
    plan2_price_annual = forms.IntegerField(
        label="プラン2 単価（円／年）※空欄ならプラン選択から自動計算",
        required=False,
        min_value=0,
    )
    plan3_price = forms.IntegerField(
        label="プラン3 単価（円／回）※空欄なら自動計算",
        required=False,
        min_value=0,
    )

    # 安全ライン
    safety_ratio = forms.FloatField(
        label="安全稼働率（例：0.7＝稼働を70％までに抑える）",
        initial=0.7,
        min_value=0.1,
        max_value=1.0,
    )
