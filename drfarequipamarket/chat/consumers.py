from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
import json
from .models import ChatGroup, GroupMessage, ChatNotification
from django.core.exceptions import ValidationError

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            self.close()
            return

        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        
        # Verificar si el usuario es parte del chat
        if self.user not in [self.chatroom.seller, self.chatroom.buyer]:
            self.close()
            return

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            action = text_data_json.get('action')
            
            if action == 'message':
                self._handle_message(text_data_json)
            elif action == 'typing':
                self._handle_typing(text_data_json)
            elif action == 'read':
                self._handle_read(text_data_json)
            else:
                self.send(text_data=json.dumps({
                    'error': 'Invalid action'
                }))
        except json.JSONDecodeError:
            self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }))
        except ValidationError as e:
            self.send(text_data=json.dumps({
                'error': str(e)
            }))
        except Exception as e:
            self.send(text_data=json.dumps({
                'error': 'Internal server error'
            }))

    def _handle_message(self, data):
        body = data.get('body')
        message_type = data.get('message_type', 'text')
        file_url = data.get('file_url')

        if not body and message_type == 'text':
            self.send(text_data=json.dumps({
                'error': 'Message body is required for text messages'
            }))
            return

        if message_type in ['image', 'file'] and not file_url:
            self.send(text_data=json.dumps({
                'error': f'File URL is required for {message_type} messages'
            }))
            return

        message = GroupMessage.objects.create(
            group=self.chatroom,
            author=self.user,
            body=body,
            message_type=message_type,
            file_url=file_url
        )

        # Crear notificación para el otro usuario
        recipient = self.chatroom.buyer if self.user == self.chatroom.seller else self.chatroom.seller
        ChatNotification.objects.create(
            chat_group=self.chatroom,
            recipient=recipient,
            sender=self.user,
            notification_type='message',
            message=message
        )

        event = {
            'type': 'message_handler',
            'message': {
                'id': message.id,
                'body': message.body,
                'message_type': message.message_type,
                'file_url': message.file_url,
                'created': message.created.isoformat(),
                'author': {
                    'id': message.author.id,
                    'email': message.author.email
                }
            }
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def _handle_typing(self, data):
        is_typing = data.get('is_typing', False)
        event = {
            'type': 'typing_handler',
            'user': {
                'id': self.user.id,
                'email': self.user.email
            },
            'is_typing': is_typing
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def _handle_read(self, data):
        message_ids = data.get('message_ids', [])
        if not message_ids:
            return

        messages = self.chatroom.chat_messages.filter(id__in=message_ids)
        for message in messages:
            message.is_read = True
            message.read_by.add(self.user)
            message.save()

        # Crear notificación de lectura
        recipient = self.chatroom.buyer if self.user == self.chatroom.seller else self.chatroom.seller
        ChatNotification.objects.create(
            chat_group=self.chatroom,
            recipient=recipient,
            sender=self.user,
            notification_type='read'
        )

        event = {
            'type': 'read_handler',
            'user': {
                'id': self.user.id,
                'email': self.user.email
            },
            'message_ids': message_ids
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def message_handler(self, event):
        self.send(text_data=json.dumps(event['message']))

    def typing_handler(self, event):
        self.send(text_data=json.dumps({
            'action': 'typing',
            'user': event['user'],
            'is_typing': event['is_typing']
        }))

    def read_handler(self, event):
        self.send(text_data=json.dumps({
            'action': 'read',
            'user': event['user'],
            'message_ids': event['message_ids']
        }))