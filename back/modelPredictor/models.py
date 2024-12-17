from django.db import models

import torch
import torchvision.models as models
import torch.nn as nn
import os


class TumorModel(nn.Module):
    def __init__(self):
        super(TumorModel, self).__init__()
        self.resnet = models.resnet18(pretrained=True)
        self.resnet.fc = nn.Linear(self.resnet.fc.in_features, 2)  # Изменяем последний слой для классификации на 2 класса

    def forward(self, x):
        return self.resnet(x)


# def load_model():
#     model = TumorModel()
#     model.load_state_dict(torch.load('tumor_model.pth', map_location='cpu')) 
#     model.eval()  # Установка модели в режим оценки
#     return model
def load_model():
    # Определяем путь к файлу модели относительно текущей директории
    model_path = os.path.join(os.path.dirname(__file__), 'tumor_model.pth')
    model = TumorModel()
    model.load_state_dict(torch.load(model_path, map_location='cpu'), strict=False) 
    model.eval()  # Установка модели в режим оценки
    return model

model = load_model()