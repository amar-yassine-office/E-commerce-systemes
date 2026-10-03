from django.urls import path
from .views import create_crypto_payment, nowpayments_webhook

urlpatterns = [
    path('create-payment/', create_crypto_payment, name='create_crypto_payment'),
    path('webhook/', nowpayments_webhook, name='nowpayments_webhook'),
]