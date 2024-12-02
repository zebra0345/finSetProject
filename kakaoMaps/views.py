from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
# Create your views here.

KAKAO_API_KEY = settings.KAKAO_API
@api_view(['POST'])
def searchMap(request):
    if request.method == "POST":
        # 요청 본문에서 JSON 데이터 추출
        data = request.data
        city = data.get('city')
        district = data.get('district')
        keyword = data.get('keyword')

        if not city or not district or not keyword:
            return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

        # 시/군 데이터를 조합하여 주소 검색
        address = f'{city} {district}'

        # Kakao 주소 검색 API 호출
        geocode_url = f'https://dapi.kakao.com/v2/local/search/address.json?query={address}'
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
        response = requests.get(geocode_url, headers=headers)

        if response.status_code != 200:
            return Response({'error': 'Failed to fetch coordinates'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        geocode_data = response.json()

        if len(geocode_data['documents']) == 0:
            return Response({'error': 'No results found for the address'}, status=status.HTTP_404_NOT_FOUND)

        # 해당 시/군의 좌표값 추출
        lat = geocode_data['documents'][0]['y']
        lon = geocode_data['documents'][0]['x']

        # Kakao 장소 검색 API 호출
        places_url = f'https://dapi.kakao.com/v2/local/search/keyword.json?y={lat}&x={lon}&radius=5000&query={keyword}'
        response = requests.get(places_url, headers=headers)

        if response.status_code != 200:
            return Response({'error': 'Failed to fetch places'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        places_data = response.json()

        # 장소 검색 결과 응답으로 전송
        places = [
            {'name': place['place_name'], 'lat': place['y'], 'lon': place['x']}
            for place in places_data['documents']
        ]

        return Response({'city': city, 'district': district, 'keyword': keyword, 'places': places})

    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
