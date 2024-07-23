from celery import shared_task
from .models import User, ReferralCode, Profile, Balance

#сделать одной таской

@shared_task
def add_money_to_referrer_referral_balance(id):
    referrer = User.objects.get(id=id)
    referrer_balance = referrer.balance
    referrer_balance.value += 100
    referrer_balance.save()


@

