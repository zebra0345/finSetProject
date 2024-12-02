from rest_framework import serializers
from .models import DepositOptions, DepositProducts, SavingOptions, SavingProducts

# 전체 조회에 사용
class DepositProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

# 전체 조회에 사용
class DepositOptionSerializers(serializers.ModelSerializer):
    product = DepositProductsSerializers(read_only=True)

    class Meta:
        model = DepositOptions
        fields = '__all__'

# 디테일 조회에 사용
class DepositOptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'

class SavingProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = '__all__'

class SavingOptionSerializers(serializers.ModelSerializer):
    product = SavingProductsSerializers(read_only=True)

    class Meta:
        model = SavingOptions
        fields = '__all__'


class SavingOptionDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
