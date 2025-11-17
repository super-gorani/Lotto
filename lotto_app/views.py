from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import LottoRound, LottoResult, LottoPurchase
import random

def generate_numbers():
    return sorted(random.sample(range(1, 46), 6))


def index(request):
    return render(request, "lotto_app/index.html")


@login_required
def buy(request):
    if not LottoRound.objects.exists():
        LottoRound.objects.create(round=1)
    latest_round = LottoRound.objects.latest('round')

    numbers = generate_numbers()
    numbers_str = ",".join(map(str, numbers))

    LottoPurchase.objects.create(
        user=None,  # 로그인 필요없으므로 사용자 NULL로 처리 가능
        lotto_round=latest_round,
        numbers=numbers_str
    )

    return render(request, "lotto_app/buy.html", {
        "numbers": numbers,
        "round": latest_round.round
    })


@login_required
def mypage(request):
    purchases = LottoPurchase.objects.filter(user=request.user).order_by('-id')
    return render(request, "lotto_app/mypage.html", {"purchases": purchases})


@login_required
def check_result(request, round_number):
    try:
        lotto_round = LottoRound.objects.get(round=round_number)
        result = LottoResult.objects.get(round=lotto_round)
    except:
        return HttpResponse("아직 추첨되지 않은 회차입니다.")

    user_purchases = LottoPurchase.objects.filter(
        user=request.user,
        lotto_round=lotto_round
    )

    context = {
        "result": result,
        "user_purchases": user_purchases,
        "round": round_number
    }

    return render(request, "lotto_app/result.html", context)


# ---------------- 관리자 기능 ----------------

def admin_draw(request):

    # 새 회차 생성
    if LottoRound.objects.exists():
        last_round = LottoRound.objects.latest("round").round
        new_round = LottoRound.objects.create(round=last_round + 1)
    else:
        new_round = LottoRound.objects.create(round=1)

    # 숫자 생성
    nums = generate_numbers()
    bonus_candidates = [n for n in range(1, 46) if n not in nums]
    bonus = random.choice(bonus_candidates)

    LottoResult.objects.create(
        round=new_round,
        numbers=",".join(map(str, nums)),
        bonus=bonus
    )

    return render(request, "lotto_app/admin_draw.html", {
        "round": new_round.round,
        "numbers": nums,
        "bonus": bonus
    })


def admin_sales(request):
    rounds = LottoRound.objects.all().order_by('-round')
    sales = []

    for r in rounds:
        count = LottoPurchase.objects.filter(lotto_round=r).count()
        sales.append({
            "round": r.round,
            "count": count,
            "revenue": count * 1000  # 로또 1장 = 1000원 가정
        })

    return render(request, "lotto_app/admin_sales.html", {"sales": sales})
