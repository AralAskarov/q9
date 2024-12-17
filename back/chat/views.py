from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from assistant.models import Chat
from login.models import CustomUser
from django.db.models import Q
from rest_framework.response import Response
from .serializers import ChatSerializer
from rest_framework import status
from rest_framework.views import APIView
User = get_user_model()

@csrf_exempt
def create_chat(request):
    # Проверяем наличие заголовка Authorization
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Требуется аутентификация: заголовок Authorization отсутствует или неверный'}, status=403)

    token = auth_header.split(' ')[1]  # Извлекаем токен из заголовка

    try:
        # Декодируем и валидируем токен
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)

        if not user.is_active:
            return JsonResponse({'error': 'Пользователь деактивирован'}, status=403)

    except User.DoesNotExist:
        return JsonResponse({'error': 'Пользователь не найден'}, status=403)

    except Exception as e:
        return JsonResponse({'error': f'Ошибка аутентификации: {str(e)}'}, status=403)

    # Создаем новый чат с названием по умолчанию "New Chat"
    chat = Chat.objects.create(user=user, title="New Chat")

    # Возвращаем данные созданного чата
    return JsonResponse({
        'message': 'Чат успешно создан',
        'chat': {
            'id': chat.id,
            'title': chat.title
        }
    }, status=201)


User = get_user_model()
@csrf_exempt
def get_chat_context_api(request):
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Требуется аутентификация: заголовок Authorization отсутствует или неверный'}, status=403)

    token = auth_header.split(' ')[1]  # Извлекаем токен из заголовка

    try:
        # Декодируем и валидируем токен
        access_token = AccessToken(token)
        # Получаем идентификатор пользователя из токена
        user_id = access_token['user_id']
        user = CustomUser.objects.get(id=user_id)

        # Проверяем, активен ли пользователь
        if not user.is_active:
            return JsonResponse({'error': 'Пользователь деактивирован'}, status=403)

    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Пользователь не найден'}, status=403)

    except Exception as e:
        return JsonResponse({'error': f'Ошибка аутентификации: {str(e)}'}, status=403)

    # Получаем название чата из запроса
    chat_title = request.GET.get('chat_title')

    if not chat_title:
        return JsonResponse({'error': 'Необходимо передать название чата'}, status=400)

    # Ищем чат по названию и пользователю
    try:
        chat = Chat.objects.get(Q(user=user) & Q(title__iexact=chat_title.strip()))
    except Chat.DoesNotExist:
        return JsonResponse({'error': 'Чат с таким названием не найден'}, status=404)

    # Получаем все сообщения чата
    messages = chat.messages.all().order_by('created_at')

    # Формируем контекст в виде JSON
    context = []
    for message in messages:
        context.append({
            'role': message.role,
            'content': message.content,
            'response': message.response,
            'image_url': message.image.url if message.image else None
        })

    return JsonResponse({'chat_title': chat_title, 'context': context}, safe=False)


class ChatListView(APIView):
    def get(self, request, *args, **kwargs):
        chats = Chat.objects.all()  # Получаем все чаты
        serializer = ChatSerializer(chats, many=True)  # Преобразуем их в JSON
        return Response(serializer.data, status=status.HTTP_200_OK)