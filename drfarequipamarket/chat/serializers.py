from rest_framework import serializers
from .models import ChatGroup, GroupMessage
from drfarequipamarket.users.models import CustomUser
from drfarequipamarket.product.models import Product

class ChatGroupSerializer(serializers.ModelSerializer):
    group_name = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='name'
    )
    
    class Meta:
        model = ChatGroup
        fields = ['id', 'group_name', 'seller', 'buyer']

class GroupMessageSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(),
        slug_field='email'
    )
    group = serializers.PrimaryKeyRelatedField(queryset = ChatGroup.objects.all())
    
    class Meta:
        model = GroupMessage
        fields = ['id', 'body', 'created', 'author', 'group']