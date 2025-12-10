

from django.shortcuts import render
from .forms import CapacityForm


def capacity_view(request):
    result = None

    if request.method == "POST":
        form = CapacityForm(request.POST)
        if form.is_valid():
            annual_hours = form.cleaned_data["annual_hours"]

            plan1_hours = form.cleaned_data["plan1_hours"]
            plan2_hours = form.cleaned_data["plan2_hours"]
            plan3_hours = form.cleaned_data["plan3_hours"]

            plan2_clients = form.cleaned_data["plan2_clients"]
            plan1_cases = form.cleaned_data["plan1_cases"]
            plan3_cases = form.cleaned_data["plan3_cases"]

            # プラン別理論最大件数
            max_plan1 = annual_hours / plan1_hours
            max_plan2 = annual_hours / plan2_hours
            max_plan3 = annual_hours / plan3_hours

            # 現在の想定構成で使っている時間
            used_hours = (
                plan2_clients * plan2_hours
                + plan1_cases * plan1_hours
                + plan3_cases * plan3_hours
            )

            remaining_hours = annual_hours - used_hours

            # 余白時間であと何件いけるか（プラン1と3の平均工数でざっくり）
            avg_single_case_hours = (plan1_hours + plan3_hours) / 2
            additional_single_cases = (
                remaining_hours / avg_single_case_hours if remaining_hours > 0 else 0
            )

            result = {
                "max_plan1": max_plan1,
                "max_plan2": max_plan2,
                "max_plan3": max_plan3,
                "used_hours": used_hours,
                "remaining_hours": remaining_hours,
                "additional_single_cases": additional_single_cases,
            }
    else:
        form = CapacityForm()

    return render(request, "capacity/capacity.html", {"form": form, "result": result})
