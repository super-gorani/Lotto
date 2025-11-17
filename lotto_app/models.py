from django.db import models
from django.contrib.auth.models import User
import random

class LottoRound(models.Model):
    round = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.round}회차"

class LottoResult(models.Model):
    round = models.OneToOneField(LottoRound, on_delete=models.CASCADE)
    numbers = models.CharField(max_length=30)   # "1,5,10,33,40,45"
    bonus = models.IntegerField()

    def number_list(self):
        return list(map(int, self.numbers.split(",")))

class LottoPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lotto_round = models.ForeignKey(LottoRound, on_delete=models.CASCADE)
    numbers = models.CharField(max_length=30)   # 자동 생성 번호
    purchased_at = models.DateTimeField(auto_now_add=True)

    def number_list(self):
        return list(map(int, self.numbers.split(",")))
