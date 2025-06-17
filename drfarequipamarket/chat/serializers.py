from rest_framework import serializers
from .models import ChatGroup, GroupMessage, ChatNotification
from drfarequipamarket.users.models import CustomUser
from drfarequipamarket.product.models import Product
from drfarequipamarket.users.serializers import UserSerializer

class ChatGroupSerializer(serializers.ModelSerializer):
    group_name = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    buyer_username = serializers.SerializerMethodField()
    seller_username = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatGroup
        fields = [
            'id', 'group_name', 'seller', 'buyer',
            'buyer_username', 'seller_username', 'last_message', 'unread_count'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_buyer_username(self, obj):
        return obj.buyer.username

    def get_seller_username(self, obj):
        return obj.seller.username

    def get_last_message(self, obj):
        last_message = obj.chat_messages.filter(is_deleted=False).first()
        if last_message:
            return GroupMessageSerializer(last_message).data
        return None

    def get_unread_count(self, obj):
        user = self.context['request'].user
        return obj.chat_messages.filter(is_read=False).exclude(author=user).count()

class GroupMessageSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    read_by = UserSerializer(many=True, read_only=True)
    group = serializers.PrimaryKeyRelatedField(queryset = ChatGroup.objects.all())
    
    class Meta:
        model = GroupMessage
        fields = ['id', 'group', 'author', 'body', 'message_type', 'file_url', 
                 'created', 'is_read', 'read_by', 'is_deleted']
        read_only_fields = ['author', 'created', 'is_read', 'read_by']

class ChatNotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    message = GroupMessageSerializer(read_only=True)

    class Meta:
        model = ChatNotification
        fields = ['id', 'chat_group', 'recipient', 'sender', 'notification_type',
                 'message', 'is_read', 'created_at']
        read_only_fields = ['created_at']