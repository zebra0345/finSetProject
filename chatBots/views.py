from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from finSetApp.models import SavingOptions, DepositOptions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from finSetApp.serializers import SavingOptionSerializers, DepositOptionSerializers
import requests
from openai import OpenAI
# Create your views here.
API_KEY = settings.OPEN_API_KEY
Saving = SavingOptions.objects.all()
Deposit = DepositOptions.objects.all()
seralizer1 = SavingOptionSerializers(Saving, many=True)
seralizer2 = DepositOptionSerializers(Deposit, many=True)
@api_view(['POST'])
def chatBot(request):
    product = {'적금': f'{seralizer1.data}', '예금': f'{seralizer2.data}'}

    content = request.data
    product_details = f"금융상품 목록: {product}"  # 실제 API 데이터
    client = OpenAI(
        api_key=API_KEY,
    )
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"## 페르소나 : 당신은 지금부터 금융상품과 API에 대한 전문적 지식을 가지고 있습니다. 또한 데이터분석에 대한 전문적 지식을 지녔습니다. ## 역할 : 사용자의 요구에 대한 최적의 금융상품 제공, ## 제약사항 : 주어진 예금, 적금 데이터를 분석하고, 그 데이터에서 사용자에게 가장 잘 맞는 금융상품 추천할것, 데이터는 옵션과 상품이름으로 이루어져있음. 은행 이름과 옵션에 대한 소개도 같이 할것",
            },
            {
                "role": "user",
                "content": f"{content}\n\n{product_details}",
            }
        ],
    )

    print(chat_completion.choices[0].message.content)
    return JsonResponse({'result':chat_completion.choices[0].message.content})