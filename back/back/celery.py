from __future__ import absolute_import
import os
from celery import Celery

# Указываем настройки вашего проекта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')

app = Celery('back')

# Загружаем конфигурацию из settings.py, используя пространство имён 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит все задачи в файлах tasks.py
app.autodiscover_tasks()