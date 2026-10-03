from django.shortcuts import render

# Create your views here.
from decimal import Decimal
import os
from django.conf import settings
from django.http import JsonResponse
from .models import CryptoTransaction
import requests


def create_crypto_payment(request):
  if request.method == 'POST':
    # بيانات افتراضية قادمة من Frontend (يمكنك تعديلها لاحقاً لتأتي من طلب العميل الحقيقي)
    price_amount = '100.00'  # المبلغ الإجمالي بالدولار
    price_currency = 'usd'  # عملة التسعير
    pay_currency = 'btc'  # العملة الرقمية المختارة للدفع (مثل btc أو usdt)

    # رابط الـ API الرسمي لـ NOWPayments
    url = 'https://api.nowpayments.io/v1/payment'

    # جلب مفتاح الـ API من إعدادات المشروع
    api_key = settings.NOWPAYMENTS_API_KEY

    headers = {'x-api-key': api_key, 'Content-Type': 'application/json'}

    payload = {
        'price_amount': float(price_amount),
        'price_currency': price_currency,
        'pay_currency': pay_currency,
    }

    try:
      # إرسال الطلب إلى خوادم NOWPayments
      response = requests.post(url, json=payload, headers=headers)
      data = response.json()

      if response.status_code in [200, 201]:
        # استخراج البيانات من استجابة NOWPayments
        payment_id = data.get('payment_id')
        pay_address = data.get('pay_address')
        pay_amount = data.get('pay_amount')
        payment_status = data.get('payment_status', 'waiting')

        # حفظ المعاملة مباشرة في قاعدة البيانات
        CryptoTransaction.objects.create(
            payment_id=payment_id,
            payment_status=payment_status,
            pay_address=pay_address,
            price_amount=Decimal(price_amount),
            price_currency=price_currency,
            pay_currency=pay_currency,
            pay_amount=Decimal(str(pay_amount)),
        )

        return JsonResponse(
            {
                'status': 'success',
                'payment_id': payment_id,
                'pay_address': pay_address,
                'pay_amount': pay_amount,
                'pay_currency': pay_currency,
            },
            status=201,
        )
      else:
        return JsonResponse(
            {
                'status': 'error',
                'message': data.get(
                    'message', 'Failed to create payment on NOWPayments'
                ),
            },
            status=400,
        )

    except Exception as e:
      return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

  return JsonResponse(
      {'status': 'error', 'message': 'Invalid request method'}, status=405
  )




import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def nowpayments_webhook(request):
  try:
    data = json.loads(request.body)
    payment_id = data.get('payment_id')
    payment_status = data.get('payment_status')

    if not payment_id:
      return JsonResponse(
          {'status': 'error', 'message': 'Missing payment_id'}, status=400
      )

    try:
      transaction = CryptoTransaction.objects.get(payment_id=str(payment_id))
      transaction.payment_status = payment_status
      transaction.save()

      if payment_status == 'confirmed':
        # منطق تفعيل الطلب أو شحن المنتج
        pass

      return JsonResponse(
          {'status': 'success', 'message': 'Transaction updated successfully'},
          status=200,
      )

    except CryptoTransaction.DoesNotExist:
      return JsonResponse(
          {'status': 'error', 'message': 'Transaction not found'}, status=404
      )

  except Exception as e:
    return JsonResponse({'status': 'error', 'message': str(e)}, status=500)