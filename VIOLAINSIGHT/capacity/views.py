# capacity/views.py
from django.shortcuts import render
from .forms import CapacityForm

from .pricing.calculator import get_monthly_fee, get_initial_analysis


def suggest_case_mix(
    annual_hours,
    target_income,
    plan1_price,
    plan2_price_annual,
    plan3_price,
    plan1_hours,
    plan2_hours,
    plan3_hours,
    max_plan1=10,
    max_plan2=10,
    max_plan3=10,
):
    """
    目標年収に一番近い件数構成をざっくり総当たりで探す。
    （0〜10件くらいなら計算量は十分軽い）
    """
    best = None

    for p2 in range(max_plan2 + 1):
        for p1 in range(max_plan1 + 1):
            for p3 in range(max_plan3 + 1):
                used_hours = p2 * plan2_hours + p1 * plan1_hours + p3 * plan3_hours
                if used_hours > annual_hours:
                    continue

                income = (
                    p2 * plan2_price_annual
                    + p1 * plan1_price
                    + p3 * plan3_price
                )

                diff = abs(target_income - income)

                if best is None or diff < best["diff"]:
                    best = {
                        "plan2_clients": p2,
                        "plan1_cases": p1,
                        "plan3_cases": p3,
                        "used_hours": used_hours,
                        "income": income,
                        "diff": diff,
                    }

    return best


def capacity_view(request):
    result = None

    if request.method == "POST":
        form = CapacityForm(request.POST)
        if form.is_valid():
            annual_hours = form.cleaned_data["annual_hours"]
            target_income = form.cleaned_data["target_income"]

            plan1_hours = form.cleaned_data["plan1_hours"]
            plan2_hours = form.cleaned_data["plan2_hours"]
            plan3_hours = form.cleaned_data["plan3_hours"]

            plan2_clients = form.cleaned_data["plan2_clients"]
            plan1_cases = form.cleaned_data["plan1_cases"]
            plan3_cases = form.cleaned_data["plan3_cases"]

            safety_ratio = form.cleaned_data["safety_ratio"]

            # ★ 新しく追加したフィールド（伴走カテゴリ & 初期分析プラン）
            monthly_category = form.cleaned_data.get("monthly_category")  # "small" / "medium" / "large"
            initial_plan = form.cleaned_data.get("initial_plan")          # "light" / "full"

            # 1) 必要なベース時給（参考情報として残しておく）
            base_hourly_rate = target_income / annual_hours  # 円/時

            # 2) 単価（未入力なら「定数ベースの標準値」で自動計算）

            # フォームからの任意入力
            input_plan1_price = form.cleaned_data["plan1_price"]          # 初期分析 1回あたり
            input_plan2_price_annual = form.cleaned_data["plan2_price_annual"]  # 年間伴走フィー
            input_plan3_price = form.cleaned_data["plan3_price"]          # 棚卸診断 1回あたり

            # --- Plan2：伴走フィー（small/medium/large） ---
            # デフォルトは定数から取得 → 12ヶ月分にする
            default_monthly_fee = get_monthly_fee(monthly_category or "small")
            default_plan2_price_annual = default_monthly_fee * 12

            # --- Plan1：初期分析（2年ごと） ---
            default_plan1_price = get_initial_analysis(initial_plan or "light")

            # --- Plan3：棚卸診断は、とりあえず「ベース時給×工数×マージン」で自動計算のまま ---
            margin_plan3 = 1.3
            auto_plan3_price = int(base_hourly_rate * plan3_hours * margin_plan3)

            # ★「フォームに値が入っていたら優先、空ならデフォルト」
            plan1_price = input_plan1_price or default_plan1_price
            plan2_price_annual = input_plan2_price_annual or default_plan2_price_annual
            plan3_price = input_plan3_price or auto_plan3_price

            # 3) 「今の構成」での時間と収入
            used_hours = (
                plan2_clients * plan2_hours
                + plan1_cases * plan1_hours
                + plan3_cases * plan3_hours
            )
            remaining_hours = annual_hours - used_hours

            estimated_income = (
                plan2_clients * plan2_price_annual
                + plan1_cases * plan1_price
                + plan3_cases * plan3_price
            )

            income_diff = estimated_income - target_income

            # 4) 安全ゾーン判定
            safe_hours = annual_hours * safety_ratio

            if used_hours <= safe_hours and abs(income_diff) <= target_income * 0.1:
                zone = "safe"      # 🟢 安全ゾーン
            elif used_hours <= annual_hours:
                zone = "warning"   # 🟡 注意ゾーン
            else:
                zone = "danger"    # 🔴 危険（時間オーバー）

            # 5) 目標年収に近い「おすすめ構成」をサジェスト
            suggestion = suggest_case_mix(
                annual_hours=annual_hours,
                target_income=target_income,
                plan1_price=plan1_price,
                plan2_price_annual=plan2_price_annual,
                plan3_price=plan3_price,
                plan1_hours=plan1_hours,
                plan2_hours=plan2_hours,
                plan3_hours=plan3_hours,
                max_plan1=10,
                max_plan2=10,
                max_plan3=10,
            )

            # ---- ここを result 作成の直前に追記 ----
            category_label_map = {
                "small": "スモール",
                "medium": "ミドル",
                "large": "ラージ",
            }
            monthly_label = category_label_map.get(monthly_category or "small", "スモール")

            # 月額フィー（デフォルト）も UI に出したい場合
            plan2_monthly_fee = default_monthly_fee


            result = {
                "base_hourly_rate": base_hourly_rate,
                "plan1_price": plan1_price,
                "plan2_price_annual": plan2_price_annual,
                "plan3_price": plan3_price,
                "used_hours": used_hours,
                "remaining_hours": remaining_hours,
                "estimated_income": estimated_income,
                "income_diff": income_diff,
                "zone": zone,
                "safe_hours": safe_hours,
                "suggestion": suggestion,
                # UIで使いやすいように、カテゴリ情報も返しておくと◎
                "monthly_category": monthly_category,
                "initial_plan": initial_plan,
                "monthly_category": monthly_category,
                "monthly_label": monthly_label,
                "plan2_monthly_fee": plan2_monthly_fee,
            }
    else:
        form = CapacityForm()

    return render(request, "capacity/capacity.html", {"form": form, "result": result})
