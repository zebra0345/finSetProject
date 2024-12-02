from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from .seralizers import ProfileSerializers, UserSerializers, ProfileUpdateSerializer
from .models import Profile
from finSetApp.models import DepositProducts, SavingProducts


# Create your views here.

User = get_user_model()

# 회원탈퇴
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def delete_user(request):
    user = request.user

    # 사용자 삭제
    user.delete()

    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# 유저 프로필 view
@api_view(['GET', 'POST'])
def profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        profile = Profile.objects.get(pk=user.pk)
        serializer = ProfileSerializers(profile)
        return Response(serializer.data)
    elif request.method == "POST":
        profile = Profile.objects.get(pk=user.pk)
        serializer = ProfileUpdateSerializer(instance=profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(User=user)
            return Response(serializer.data)


# 예금추가 view
@api_view(['POST'])
def profile_add_deposit(request, profile_pk, deposit_pk):
    profile = Profile.objects.get(pk=profile_pk)
    deposit1 = DepositProducts.objects.get(pk=deposit_pk)

    deposit_list = profile.deposit.all()
    if deposit1 not in deposit_list:
        # 없으면 더함
        profile.deposit.add(deposit1)
        return Response({"message": "Deposit added successfully."}, status=status.HTTP_200_OK)
    else:
        # 이미 존재하면 제거
        profile.deposit.remove(deposit1)
        return Response({"message": "Deposit removed successfully."}, status=status.HTTP_200_OK)

# 적금추가 view
@api_view(['POST'])
def profile_add_saving(request, profile_pk, saving_pk):
    profile = Profile.objects.get(pk=profile_pk)
    saving1 = SavingProducts.objects.get(pk=saving_pk)

    saving_list = profile.saving.all()
    if saving1 not in saving_list:
        # 없으면 더함
        profile.saving.add(saving1)
        return Response({"message": "Saving added successfully."}, status=status.HTTP_200_OK)
    else:
        # 이미 존재하면 제거
        profile.saving.remove(saving1)
        return Response({"message": "Saving removed successfully."}, status=status.HTTP_200_OK)