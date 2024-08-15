from celery import shared_task
from .models import User, ReferralCode, Profile, Balance


@shared_task
def add_money_to_referrer_referral_balance(id):
    referral = User.objects.get(id=id)
    referral_balance = referral.balance
    referral_balance.value += 25
    referral_balance.save()
    referrer = referral.referrer
    referrer_balance = referrer.balance
    referrer_balance.value += 100
    referrer_balance.save()
