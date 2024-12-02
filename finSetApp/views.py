from django.db import transaction
from django.conf import settings
from django.core.mail import send_mail
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.http.response import JsonResponse
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions
from .serializers import DepositOptionSerializers, DepositProductsSerializers, SavingOptionSerializers, SavingProductsSerializers, DepositOptionDetailSerializer, SavingOptionDetailSerializers
from accounts.models import Profile
# API_KEY 설정
API_KEY = settings.API_KEY

# 예금URL
depositUrl = f"https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1"
# 적금URL
savingUrl = f"http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1"
# 메일 보내는 함수
def send_rate_update_email(user, product_name, old_rate, new_rate):
    subject = f'{product_name} 금리 변경 알림 메일'
    message = f'안녕하세요 {user.username}님, \n\n금리가 {old_rate}%에서 {new_rate}%로 변경되었습니다.'
    recipient_list = [user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
@api_view(['POST', 'GET'])
# @permission_classes([IsAdminUser])
# 초기 데이터 생성하는 view입니다.
# 예금데이터 생성합니다.
def depositDataCreated(request):
    datas = requests.get(depositUrl).json()
    
    # DepositProducts의 fin_prdt_cd만 세팅하여 메모리 최적화
    existing_products = {product.fin_prdt_cd for product in DepositProducts.objects.all()}
    
    # DepositProducts 객체 배치 생성 준비
    products_to_create = []
    for data in datas.get('result').get('baseList'):
        fin_prdt_cd = data['fin_prdt_cd']
        
        # 이미 존재하는 상품이 있으면 넘어감
        if fin_prdt_cd not in existing_products:
            product = DepositProducts(
                fin_prdt_cd=fin_prdt_cd,
                kor_co_nm=data["kor_co_nm"],
                fin_prdt_nm=data["fin_prdt_nm"],
                etc_note=data["etc_note"],
                join_deny=data["join_deny"],
                join_member=data["join_member"],
                join_way=data["join_way"],
                spcl_cnd=data["spcl_cnd"]
            )
            products_to_create.append(product)

    # DepositProducts 객체가 있다면 한 번에 생성
    if products_to_create:
        DepositProducts.objects.bulk_create(products_to_create)
    
    # DepositOptions 객체 배치 생성 준비
    options_to_create = []
    for data in datas.get('result').get('optionList'):
        fin_prdt_cd = data["fin_prdt_cd"]
        product_deposit = DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
        
        if product_deposit:
            intr_rate = data["intr_rate"] if data["intr_rate"] is not None else -1
            intr_rate2 = data["intr_rate2"] if data["intr_rate2"] is not None else -1
            save_trm = data["save_trm"]
            intr_rate_type_nm = data["intr_rate_type_nm"]

            # 이미 존재하는 옵션은 넘어감
            if not DepositOptions.objects.filter(product=product_deposit, fin_prdt_cd=fin_prdt_cd, 
                                                intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, 
                                                intr_rate2=intr_rate2, save_trm=save_trm).exists():
                options_to_create.append(DepositOptions(
                    product=product_deposit,
                    fin_prdt_cd=fin_prdt_cd,
                    intr_rate_type_nm=intr_rate_type_nm,
                    intr_rate=intr_rate,
                    intr_rate2=intr_rate2,
                    save_trm=save_trm
                ))

    # DepositOptions 객체가 있다면 한 번에 생성
    if options_to_create:
        DepositOptions.objects.bulk_create(options_to_create)

    return Response({"message": "데이터베이스 생성 성공"})

@api_view(['GET', 'POST'])
# @permission_classes([IsAdminUser])
# 적금데이터 생성하는 view입니다.
def savingsDataCreate(request):
    datas = requests.get(savingUrl).json()
    
    base_list = datas.get('result').get('baseList')
    option_list = datas.get('result').get('optionList')

    # set으로 메모리 최적화
    existing_product = {saving.fin_prdt_cd for saving in SavingProducts.objects.all()}

    # 생성해야되는 객체 한번에생성
    products_to_create = []
    for base in base_list:
        fin_prdt_cd = base['fin_prdt_cd']
                # 이미 존재하는 상품이 있으면 넘어감
        if fin_prdt_cd not in existing_product:
            product = SavingProducts(
                fin_prdt_cd=fin_prdt_cd,
                kor_co_nm=base["kor_co_nm"],
                fin_prdt_nm=base["fin_prdt_nm"],
                etc_note=base["etc_note"],
                join_deny=base["join_deny"],
                join_member=base["join_member"],
                join_way=base["join_way"],
                spcl_cnd=base["spcl_cnd"]
            )
            products_to_create.append(product)

    # DepositProducts 객체가 있다면 한 번에 생성
    if products_to_create:
        SavingProducts.objects.bulk_create(products_to_create)

    # DepositOptions 객체 배치 생성 준비
    options_to_create = []
    for option in option_list:
        fin_prdt_cd = option["fin_prdt_cd"]
        product_deposit = SavingProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
        
        if product_deposit:
            intr_rate = option["intr_rate"] if option["intr_rate"] is not None else -1
            intr_rate2 = option["intr_rate2"] if option["intr_rate2"] is not None else -1
            save_trm = option["save_trm"]
            intr_rate_type_nm = option["intr_rate_type_nm"]

            # 이미 존재하는 옵션은 넘어감
            if not SavingOptions.objects.filter(product=product_deposit, fin_prdt_cd=fin_prdt_cd, 
                                                intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, 
                                                intr_rate2=intr_rate2, save_trm=save_trm).exists():
                options_to_create.append(SavingOptions(
                    product=product_deposit,
                    fin_prdt_cd=fin_prdt_cd,
                    intr_rate_type_nm=intr_rate_type_nm,
                    intr_rate=intr_rate,
                    intr_rate2=intr_rate2,
                    save_trm=save_trm
                ))

    # DepositOptions 객체가 있다면 한 번에 생성
    if options_to_create:
        SavingOptions.objects.bulk_create(options_to_create)
    return Response({"message": "데이터베이스 생성 성공"})


# 예금데이터 전체조회하는 view입니다.
@api_view(['GET'])
def depositProductsAll(request):
    products = DepositProducts.objects.all()
    serializer = DepositProductsSerializers(products, many=True)

    return Response(serializer.data)

# 예금데이터 상세조회하는 view입니다.
@api_view(['GET', 'DELETE'])
def depositProductDetail(request, pk):
    if request.method == 'GET':
        product = DepositProducts.objects.get(pk=pk)
        serializer = DepositProductsSerializers(product)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        pk = product.pk
        product.delete()
        return JsonResponse({'msg':f'{pk}번째 데이터가 삭제완료되었습니다.'})

# 해당 예금데이터에 맞는 옵션리스트 출력하는 view입니다.
@api_view(['GET'])
def depositProductOptions(request, pk):
    if request.method == 'GET':
        deposit = DepositProducts.objects.get(pk=pk)
        options = deposit.product.all()
        
        serializer = DepositOptionSerializers(options, many=True)

        return Response(serializer.data)
    
# 예금옵션 pk에 해당하는 옵션리스트 가져오기
# 도전과제 [수정완료, 이메일 보내야함]
@api_view(['GET', 'PUT', 'DELETE'])
def optionDetail(request, pk):
    option = DepositOptions.objects.get(pk=pk)
    old_rate = option.intr_rate
    if request.method == 'GET':
        serializer = DepositOptionDetailSerializer(option)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DepositOptionSerializers(instance=option, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            new_rate = serializer.validated_data.get('intr_rate', old_rate)
            print("ASADDAS")
            if old_rate != new_rate:
                having_profiles = Profile.objects.filter(deposit=option.product)
                print(f'객체 반환 : {having_profiles}')
                for profile in having_profiles:
                    print("한화")
                    send_rate_update_email(profile.User, option.product.fin_prdt_nm, old_rate, new_rate)
            return Response(serializer.data)
    elif request.method == 'DELETE':
        pk = option.pk
        option.delete()
        return JsonResponse({'msg':f'{pk}번째 데이터가 삭제 완료되었습니다.'})


# 적금데이터 전체조회하는 view입니다.
@api_view(['GET'])
def SavingProductsAll(request):
    products = SavingProducts.objects.all()
    serializer = SavingProductsSerializers(products, many=True)

    return Response(serializer.data)

# 적금데이터 상세조회하는 view입니다.
@api_view(['GET', 'DELETE'])
def SavingProductDetail(request, pk):
    product = DepositProducts.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = DepositProductsSerializers(product)

        return Response(serializer.data)
    elif request.method == 'DELETE':
        pk = product.pk
        product.delete()
        return JsonResponse({'msg':f'{pk}번째 데이터가 삭제완료되었습니다.'})

# 해당 적금데이터에 맞는 옵션리스트 출력하는 view입니다.
@api_view(['GET'])
def SavingProductOptions(request, pk):
    saving = SavingProducts.objects.get(pk=pk)
    options = saving.savingoptions_set.all()
    if request.method == 'GET':        
        serializer = SavingOptionSerializers(options, many=True)
        return Response(serializer.data)

# 적금옵션 디테일 view입니다.
@api_view(['GET', 'PUT', 'DELETE'])
def optionDetail(request, pk):
    option = SavingOptions.objects.get(pk=pk)
    old_rate = option.intr_rate
    if request.method == 'GET':
        serializer = SavingOptionDetailSerializers(option)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SavingOptionSerializers(instance=option, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            new_rate = serializer.validated_data.get('intr_rate', old_rate)
            print("ASADDAS")
            if old_rate != new_rate:
                having_profiles = Profile.objects.filter(saving=option.product)
                print(f'객체 반환 : {having_profiles}')
                for profile in having_profiles:
                    print("한화")
                    send_rate_update_email(profile.User, option.product.fin_prdt_nm, old_rate, new_rate)
            return Response(serializer.data)
    elif request.method == 'DELETE':
        pk = option.pk
        option.delete()
        return JsonResponse({'msg':f'{pk}번째 적금 옵션 데이터가 삭제 완료되었습니다.'})