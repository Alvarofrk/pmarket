from django.db import models
from drfarequipamarket.product import models as ProductModels
from drfarequipamarket.users import models as UserModels

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.ForeignKey(ProductModels.Product, default='', on_delete=models.CASCADE)
    seller = models.ForeignKey(UserModels.CustomUser, related_name='chat_seller', on_delete=models.CASCADE)
    buyer = models.ForeignKey(UserModels.CustomUser, related_name='chat_buyer', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group_name.name} - {self.seller.email} & {self.buyer.email}"
    class Meta:
        unique_together = ('group_name', 'seller', 'buyer')

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(UserModels.CustomUser, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.email} : {self.body}'
    
    class Meta:
        ordering = ['-created']