from django import forms

class CapacityForm(forms.Form):
    annual_hours = forms.IntegerField(label="年間稼働時間（h）", initial=600)

    plan1_hours = forms.IntegerField(label="プラン1（体質診断）工数（h/年）", initial=12)
    plan2_hours = forms.IntegerField(label="プラン2（月次伴走）工数（h/年）", initial=49)
    plan3_hours = forms.IntegerField(label="プラン3（棚卸）工数（h/年）", initial=12)

    plan2_clients = forms.IntegerField(label="月次伴走クライアント数", initial=5)
    plan1_cases = forms.IntegerField(label="年間プラン1件数", initial=4)
    plan3_cases = forms.IntegerField(label="年間プラン3件数", initial=4)
