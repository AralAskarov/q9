from django.db import models

from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model() 
# class UserImage(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='user_images/')
#     description = models.TextField(blank=True, null=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Image by {self.user.email} - {self.description}"
    
class Chat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chats', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)  
    is_cancer_related = models.BooleanField(null=True, default=None)

    def __str__(self):
        return f"Чат {self.id} пользователя {self.user.email}"
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # Отправитель (может быть пользователь или ассистент)
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('assistant', 'Assistant')])  # Роль отправителя
    content = models.TextField(blank=True, null=True)  # Текст сообщения (может быть пустым, если есть изображение)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)  # Изображение (может быть пустым)
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания сообщения

    def __str__(self):
        return f"Сообщение от {self.sender.email} в чате {self.chat.id}"