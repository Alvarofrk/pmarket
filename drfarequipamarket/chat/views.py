from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from drfarequipamarket.chat.models import ChatGroup, GroupMessage
from drfarequipamarket.users.models import CustomUser
from drfarequipamarket.chat.serializers import ChatGroupSerializer, GroupMessageSerializer

class ChatGroupViewSet(viewsets.ModelViewSet):
    queryset = ChatGroup.objects.all()
    serializer_class = ChatGroupSerializer

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Envia un mensaje en el chat group del producto
        El request debe contenter: 'author_id' y 'body'
        """
        chat_group = self.get_object()
        author_id = request.data.get('author_id')
        body = request.data.get('body')

        if not author_id or not body:
            return Response({'detail': 'author_id and body are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            author = CustomUser.objects.get(id=author_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Author not found.'}, status=status.HTTP_404_NOT_FOUND)

        if int(author_id) not in [chat_group.seller.id, chat_group.buyer.id]:
            return Response({'detail': 'Author not a member of this chat group.'}, status=status.HTTP_403_FORBIDDEN)

        message = GroupMessage.objects.create(
            group=chat_group,
            author=author,
            body=body
        )

        serializer = GroupMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Get all messages in a chat group
        """
        chat_group = self.get_object()
        messages = chat_group.chat_messages.all().order_by('created')
        serializer = GroupMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)