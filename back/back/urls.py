"""
URL configuration for back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from login.views import CustomTokenObtainPairView
from login.views import RegisterView,EmailConfirmView
from assistant.views import upload_image_or_text_api
# from assistant.views import upload_photo
from chat.views import create_chat, get_chat_context_api
from chat.views import ChatListView
from modelPredictor.views import predict_tumor

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("login/", TokenObtainPairView.as_view()),
    path("login/", CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("refresh/", TokenRefreshView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/<str:token>/', EmailConfirmView.as_view(), name='confirm_email'),
    path('assistant/', upload_image_or_text_api, name='openai_assistant'),
    # path('upload_photo/', upload_photo, name='upload photo'),
    path('create_chat/', create_chat, name='create_chat'),
    path('get_context/', get_chat_context_api, name='get_context'),
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path('predict/', predict_tumor, name='predict_tumor'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
