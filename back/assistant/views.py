from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import requests
import os
import json
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from login.models import CustomUser
from assistant.models import Chat, Message
import requests
from django.db.models import Q
import time
from PIL import Image
import torch
from torchvision import transforms
from modelPredictor.views import predict_tumor
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model() 
@csrf_exempt
def upload_image_or_text_api(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Требуется аутентификация: заголовок Authorization отсутствует или неверный'}, status=403)
    token = auth_header.split(' ')[1] 

    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = CustomUser.objects.get(id=user_id)
        if not user.is_active:
            return JsonResponse({'error': 'Пользователь деактивирован'}, status=403)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Пользователь не найден'}, status=403)

    except Exception as e:
        return JsonResponse({'error': f'Ошибка аутентификации: {str(e)}'}, status=403)
    
    description = request.POST.get('description')

    image = request.FILES.get('image')

    print('[GAY PARTY]')
    print(image)
    print('[GAY PARTY IS OVER]')

    chat_title = request.POST.get('chat_title', 'New Chat')
    chat, created = Chat.objects.get_or_create(user=user, title=chat_title)
    
    if not description and not image:
        return JsonResponse({'error': 'Необходимо предоставить описание или изображение'}, status=400)
    access_token = AccessToken(token)
    context = get_chat_context(chat_title, access_token)

    if image:
        client = Client()
        # temp_photo_path = os.path.join(settings.MEDIA_ROOT, 'image.jpg')

# Открываем изображение
        # with open(temp_photo_path, 'rb') as image_file:
            # Создаем объект SimpleUploadedFile
            # uploaded_image = SimpleUploadedFile('image.png', image_file.read(), content_type='image/jpeg')

            # Отправляем POST-запрос только с файлом (в параметре files)
        oneorzero = client.post('http://127.0.0.1:8000/predict/', {'image': image})

            # Выводим результат
            # print(response.json())t
        json_response = oneorzero.json()
        print('[GAY PARTY]')
        print(json_response)
        print('[GAY PARTY IS OVER]')
        # result = {'result': 1}
        if json_response == {'result': 1}:
            description += " Note: SAY THAT I HAVE LIVER CANCER "
            # user.last_name = " this user has liver cancer"
            chat.is_cancer_related = True
        else:
            description += " Note: SAY THAT I DONT HAVE LIVER CANCER"
            # user.last_name = " this user doent have liver cancer"
            chat.is_cancer_related = False
        chat.save()
        print(description)
        user.save()

        message = Message.objects.create(chat=chat, sender=user, role='user', content=description, image=image)

    else:
        message = Message.objects.create(chat=chat, sender=user, role='user', content=description)
    temp = description 
    a = 1
    if chat.is_cancer_related == 1:
        a = " Note: user has liver cancer"
    elif chat.is_cancer_related == 0:
        a = " Note: user doesn't have liver cancer"
    else:
        a = " "
        print("PORNO")
    description += a
    description += temp
    print(description)
    print(description)
    context = context[-4:]
    openai_response = send_message_to_openai(description, context)
    print(context)
    message.response = openai_response
    message.save()
    message_count = chat.messages.count()
    print(f"Количество сообщений в чате: {message_count}")

    if message_count == 1 and chat_title == "New Chat":
        time.sleep(8)
        print("Входим в условие: сообщений в чате ровно 1")
        
        gpt_title_prompt = f"Запрос пользователя: '{description}'. Придумай подходящее название для этого чата.должно быть меньше 255 символов. ответь просто названием"
        
        new_chat_title = send_message_to_openai(gpt_title_prompt, [])

        if len(new_chat_title) > 255:
            new_chat_title = new_chat_title[:255]

        # Обновляем название чата
        chat.title = new_chat_title
        chat.save()

        print(f"Название чата обновлено на: {chat.title}")
    else:
        print("Условие не выполнено: сообщений больше или меньше 1")

    if openai_response.startswith("Error: 429"):
        openai_response = "Error! Please try again in a minute."
    return JsonResponse({'message': 'Запрос успешно обработан!', 'result': openai_response,'chat_title':chat.title})


def send_message_to_openai(prompt, context):
    if not context: 
        context = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    api_key = '27aceb1e35e24107b228f3ce5a765ae1'
    api_version = '2024-08-01-preview'
    headers = {
        'api-key': '27aceb1e35e24107b228f3ce5a765ae1', 
        'Content-Type': 'application/json',
    }
    data = {
        "messages": context,
        "max_tokens": 500
    }
    endpoint = 'https://pliiz-pliz.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2024-08-01-preview'

    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        print(response)
        result = response.json()
        return result.get('choices')[0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"


User = get_user_model()
def get_chat_context(chat_title, access_token):
    user_id = access_token['user_id']
    user = CustomUser.objects.get(id=user_id)
    try:
        chat = Chat.objects.get(Q(user=user) & Q(title__iexact=chat_title.strip()))
    except Chat.DoesNotExist:
        return JsonResponse({'error': 'Чат с таким названием не найден'}, status=404)
    messages = chat.messages.all().order_by('created_at')  
    
    context = [
    {
        "role": "system",
        "content": "You are an AI assistant specialized in liver cancer, dedicated to providing personalized, accurate guidance on all aspects of liver cancer. Based on the user's tests, determine whether the user has liver cancer. If they do, respond with 'You have liver cancer.' If not, respond with 'You do not have liver cancer.' Once you have given this result, do not repeat it in future responses. After delivering the result, continue offering tailored support regarding diagnosis, treatment options, prevention, and lifestyle changes, ensuring compassionate and helpful advice."
    }
]
    for message in messages:
        if message.content:
            context.append({
                "role": message.role,
                "content": message.content
            })
        if message.response:
            context.append({
                "role": 'assistant',
                "content": message.response
            })

    return context
