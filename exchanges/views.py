from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
# Create your views here.
import requests
API_KEY = settings.FIN_KEY

@api_view(['GET'])
def exchanges(request):
    searchdate = request.GET.get('searchdate')
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={API_KEY}&searchdate={searchdate}&data=AP01'

    data = requests.get(url,verify=False).json()

    return Response({'result':data})