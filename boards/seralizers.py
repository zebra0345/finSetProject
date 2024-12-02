from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Board, Comment
class UserSeralizers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id']

class BoardSeralizers(serializers.ModelSerializer):
    User = UserSeralizers(read_only=True)
    class Meta:
        model = Board
        fields  = '__all__'

class CommentSeralizers(serializers.ModelSerializer):
    User = UserSeralizers(read_only=True)
    board = BoardSeralizers(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'


    