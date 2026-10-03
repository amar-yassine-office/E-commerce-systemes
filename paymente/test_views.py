from decimal import Decimal
import json
from unittest.mock import patch
from django.urls import reverse
import pytest
from paymente.models import CryptoTransaction


@pytest.mark.django_db
class TestCryptoPaymentAPI:

  @patch('paymente.views.requests.post')
  def test_create_crypto_payment_success(self, mock_post, client):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {
        'payment_id': '123456789',
        'pay_address': '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
        'pay_amount': 0.0025,
        'pay_currency': 'btc',
        'payment_status': 'waiting',
    }

    url = reverse('create_crypto_payment')
    response = client.post(url)

    assert response.status_code == 201
    data = response.json()
    assert data['status'] == 'success'
    assert data['payment_id'] == '123456789'

    transaction = CryptoTransaction.objects.get(payment_id='123456789')
    assert transaction.payment_status == 'waiting'
    assert transaction.pay_currency == 'btc'
    assert transaction.price_amount == Decimal('100.00')

  def test_nowpayments_webhook_success(self, client):
    transaction = CryptoTransaction.objects.create(
        payment_id='123456789',
        payment_status='waiting',
        pay_address='1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
        price_amount=Decimal('100.00'),
        price_currency='usd',
        pay_amount=Decimal('0.0025'),
        pay_currency='btc',
    )

    webhook_data = {
        'payment_id': '123456789',
        'payment_status': 'finished',
        'pay_amount': 0.0025,
        'actually_paid': 0.0025,
        'pay_currency': 'btc',
        'order_id': 'order_123',
    }

    url = reverse('nowpayments_webhook')
    # التصحيح هنا بإرسال content_type كـ application/json واستخدام json.dumps
    response = client.post(
        url, data=json.dumps(webhook_data), content_type='application/json'
    )

    assert response.status_code == 200

    transaction.refresh_from_db()
    assert transaction.payment_status == 'finished'