from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import torch
from torchvision import transforms
from .models import load_model

# Загружаем модель
model = load_model()

@csrf_exempt
def predict_tumor(request):
    if request.method == 'POST':
        # Получаем изображение из запроса
        image_file = request.FILES.get('image')
        if not image_file:
            return JsonResponse({'error': 'No image provided'}, status=400)

        try:
            image = Image.open(image_file)
            # Преобразуем изображение в RGB, если оно имеет альфа-канал
            if image.mode != 'RGB':
                image = image.convert('RGB')
        except Exception as e:
            return JsonResponse({'error': 'Invalid image format'}, status=400)

        # Преобразование изображения для модели
        transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
        ])
        image = transform(image).unsqueeze(0)  # Добавляем размерность для батча

        # Получаем предсказание
        with torch.no_grad():
            output = model(image)
            _, predicted = torch.max(output.data, 1)

        result = predicted.item()
        return JsonResponse({'result': result})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
