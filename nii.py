import nibabel as nib
import matplotlib.pyplot as plt
import os

# Загрузка NIfTI файла
nii_file = nib.load(r"/home/aral/Downloads/Telegram Desktop/volume-0.nii")
data = nii_file.get_fdata()

# Путь для сохранения JPEG файлов
output_dir = r"/home/aral/Downloads/Telegram Desktop/output"
os.makedirs(output_dir, exist_ok=True)  # Создаем директорию, если она не существует

# Проходим по каждому срезу по оси Z
for i in range(data.shape[2]):
    plt.imshow(data[:, :, i], cmap='gray')
    plt.axis('off')  # Отключаем оси

    # Сохраняем каждый срез как JPEG
    output_path = os.path.join(output_dir, f'slice_{i}.jpg')
    plt.savefig(output_path, format='jpeg', bbox_inches='tight', pad_inches=0)
    plt.close()  # Закрываем фигуру для предотвращения утечек памяти

print(f"Срезы успешно сохранены в директорию: {output_dir}")