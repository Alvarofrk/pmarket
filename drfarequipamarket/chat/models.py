from django.db import models
from django.core.exceptions import ValidationError
from drfarequipamarket.product import models as ProductModels
from drfarequipamarket.users import models as UserModels

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.ForeignKey(ProductModels.Product, default='', on_delete=models.CASCADE)
    seller = models.ForeignKey(UserModels.CustomUser, related_name='chat_seller', on_delete=models.CASCADE)
    buyer = models.ForeignKey(UserModels.CustomUser, related_name='chat_buyer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.group_name.name} - {self.seller.email} & {self.buyer.email}"
    class Meta:
        unique_together = ('group_name', 'seller', 'buyer')
        ordering = ['-updated_at']

class GroupMessage(models.Model):
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
    )

    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(UserModels.CustomUser, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    file_url = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_by = models.ManyToManyField(UserModels.CustomUser, related_name='read_messages')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author.email} : {self.body}'
    
    def clean(self):
        if not self.body.strip():
            raise ValidationError('Message cannot be empty')
        if self.message_type in ['image', 'file'] and not self.file_url:
            raise ValidationError(f'File URL is required for {self.message_type} messages')

    class Meta:
        ordering = ['-created']

class ChatNotification(models.Model):
    NOTIFICATION_TYPES = (
        ('message', 'New Message'),
        ('read', 'Message Read'),
        ('typing', 'User Typing'),
    )

    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(UserModels.CustomUser, on_delete=models.CASCADE, related_name='chat_notifications')
    sender = models.ForeignKey(UserModels.CustomUser, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.ForeignKey(GroupMessage, null=True, blank=True, on_delete=models.SET_NULL)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
            models.Index(fields=['notification_type']),
        ]

    def __str__(self):
        return f'{self.notification_type} notification for {self.recipient.email}'