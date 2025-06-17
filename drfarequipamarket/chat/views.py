from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from drfarequipamarket.chat.models import ChatGroup, GroupMessage, ChatNotification
from drfarequipamarket.users.models import CustomUser
from drfarequipamarket.chat.serializers import ChatGroupSerializer, GroupMessageSerializer, ChatNotificationSerializer
from django.db.models import Q, Prefetch
from django.utils import timezone

class MessagePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

class ChatGroupViewSet(viewsets.ModelViewSet):
    serializer_class = ChatGroupSerializer
    pagination_class = MessagePagination

    def get_queryset(self):
        user = self.request.user
        product_id = self.request.query_params.get('product')
        
        queryset = ChatGroup.objects.select_related(
            'seller', 'buyer', 'group_name'
        ).prefetch_related(
            Prefetch(
                'chat_messages',
                queryset=GroupMessage.objects.filter(is_deleted=False).order_by('-created')
            )
        )

        if product_id:
            return queryset.filter(group_name_id=product_id, seller=user).exclude(buyer=user)
        
        return queryset.filter(Q(seller=user) | Q(buyer=user)).filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        chat_group = self.get_object()
        body = request.data.get('body')
        message_type = request.data.get('message_type', 'text')
        file_url = request.data.get('file_url')

        if not body and message_type == 'text':
            return Response(
                {'detail': 'Message body is required for text messages.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if message_type in ['image', 'file'] and not file_url:
            return Response(
                {'detail': f'File URL is required for {message_type} messages.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        message = GroupMessage.objects.create(
            group=chat_group,
            author=request.user,
            body=body,
            message_type=message_type,
            file_url=file_url
        )

        # Crear notificación para el otro usuario
        recipient = chat_group.buyer if request.user == chat_group.seller else chat_group.seller
        ChatNotification.objects.create(
            chat_group=chat_group,
            recipient=recipient,
            sender=request.user,
            notification_type='message',
            message=message
        )

        serializer = GroupMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        chat_group = self.get_object()
        messages = chat_group.chat_messages.filter(is_deleted=False).order_by('created')
        page = self.paginate_queryset(messages)
        serializer = GroupMessageSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        chat_group = self.get_object()
        message_ids = request.data.get('message_ids', [])
        
        if not message_ids:
            return Response(
                {'detail': 'No message IDs provided.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        messages = chat_group.chat_messages.filter(id__in=message_ids)
        for message in messages:
            message.is_read = True
            message.read_by.add(request.user)
            message.save()

        # Crear notificación de lectura
        recipient = chat_group.buyer if request.user == chat_group.seller else chat_group.seller
        ChatNotification.objects.create(
            chat_group=chat_group,
            recipient=recipient,
            sender=request.user,
            notification_type='read'
        )

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def delete_message(self, request, pk=None):
        chat_group = self.get_object()
        message_id = request.data.get('message_id')
        
        try:
            message = chat_group.chat_messages.get(id=message_id)
            if message.author != request.user:
                return Response(
                    {'detail': 'You can only delete your own messages.'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            message.is_deleted = True
            message.save()
            return Response(status=status.HTTP_200_OK)
        except GroupMessage.DoesNotExist:
            return Response(
                {'detail': 'Message not found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class ChatNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = ChatNotificationSerializer
    pagination_class = MessagePagination

    def get_queryset(self):
        return ChatNotification.objects.filter(
            recipient=self.request.user,
            is_read=False
        ).select_related(
            'chat_group', 'sender', 'recipient', 'message'
        ).order_by('-created_at')

    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        notification_ids = request.data.get('notification_ids', [])
        if not notification_ids:
            return Response(
                {'detail': 'No notification IDs provided.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        notifications = self.get_queryset().filter(id__in=notification_ids)
        notifications.update(is_read=True, updated_at=timezone.now())
        return Response(status=status.HTTP_200_OK)