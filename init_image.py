# _*_ coding:utf-8 _*_
import cv2
import os
from tkinter import *
import time

CASE_PATH = "haarcascade_frontalface_default.xml"
RAW_IMAGE_DIR = 'me/'
DATASET_DIR = 'jm/'

face_cascade = cv2.CascadeClassifier(CASE_PATH)

# Кадрирование изображение 100 на 100 пикселей
def resize_without_deformation(image, size = (100, 100)):
    height, width, _ = image.shape
    longest_edge = max(height, width)
    top, bottom, left, right = 0, 0, 0, 0
    if height < longest_edge:
        height_diff = longest_edge - height
        top = int(height_diff / 2)
        bottom = height_diff - top
    elif width < longest_edge:
        width_diff = longest_edge - width
        left = int(width_diff / 2)
        right = width_diff - left

    image_with_border = cv2.copyMakeBorder(image, top , bottom, left, right, cv2.BORDER_CONSTANT, value = [0, 0, 0])

    resized_image = cv2.resize(image_with_border, size)

    return resized_image
# Закрепление кадрирования при помощи функции
def save_feces(img, name,x, y, width, height):
    image = img[y:y+height, x:x+width]
    cv2.imwrite(name, resize_without_deformation(image))

cnt = 166
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Захват камеры
ret, img = cap.read() # Чтение камеры
cv2.imshow("Camera", img) # Создание окна трансляции видео с вебкамеры

# Функция скриншота
def screenshot():
    cv2.imwrite(RAW_IMAGE_DIR + 'cp' + str(cnt) + '.bmp', img)
    return img

while True:
    time.sleep(1) # Задержка скриншота 1 сек
    screenshot()
    cnt += 1
    if cv2.waitKey(10) == 13: # При нажатии на Enter цикл прекращается P.S. Не всегда работает с первого нажатия
        break
# Закрытие всех окон
cap.release()
cv2.destroyAllWindows()

image_list = os.listdir(RAW_IMAGE_DIR) # Список всех каталогов и файлов в папке
count = 166
# Создании маски лица
for image_path in image_list:
    image = cv2.imread(RAW_IMAGE_DIR + image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,
                                         scaleFactor=1.2,
                                         minNeighbors=5,
                                         minSize=(5, 5), )
# Сохранение лиц в формате bmp
    for (x, y, width, height) in faces:
        save_feces(image, '%ss%d.bmp' % (DATASET_DIR, count), x, y, width, height)
    count += 1