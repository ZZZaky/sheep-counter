import torch
from PIL import Image
import numpy as np
import cv2

# Загрузка предобученной модели YOLOv5 (например yolov5s)
# Для реального проекта лучше дообучить модель на овцах
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = 0.25  # confidence threshold

# Предположим, что класс "овца" соответствует class_id=16 в COCO (проверьте!)
SHEEP_CLASS_ID = 18

def detect_sheep(image: Image.Image):
    """
    Принимает PIL.Image, возвращает:
    - изображение с обведёнными овцами (PIL.Image)
    - количество овец (int)
    """
    results = model(image)
    # results.xyxy[0] - тензор с координатами и классами
    detections = results.xyxy[0].cpu().numpy()

    print("Все детекции:")
    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        print(f"Класс: {model.names[int(cls)]}, confidence: {conf:.2f}")

    # Фильтруем по классу овец
    sheep_detections = [det for det in detections if int(det[5]) == SHEEP_CLASS_ID]

    # Рисуем bounding box
    img_np = np.array(image.convert("RGB"))

    for det in sheep_detections:
        x1, y1, x2, y2, conf, cls = det
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cv2.rectangle(img_np, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img_np, f"Sheep {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    img_out = Image.fromarray(img_np)

    return img_out, len(sheep_detections)
