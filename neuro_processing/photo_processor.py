import onnxruntime as ort
from PIL import Image, ImageDraw
import numpy as np
from PIL import ImageFont
# from roboflow import Roboflow
#
#
# rf = Roboflow(api_key="z1B73yP5LSQJhcOeuKL9")
# project = rf.workspace().project("detect-money")
# model = project.version(2).model

# result.plot() - нарисовать квадраты


model = ort.InferenceSession("neuro_processing/detector.onnx")
unprocessed_photo_folder = './photos/unprocessed/'
processed_photo_folder = './photos/processed/'

yolo_classes = [
    "10kop_coin", "50kop_coin", "1rub_coin", "2rub_coin", "5rub_coin",
    "5rub_note", "10rub_coin", "50rub_note", "100rub_note",
    "500rub_note", "1000rub_note", "2000rub_note", "5000rub_note",
    "backsite", "not_money"
]


def detect_objects_on_image(buf):
    input, img_width, img_height = prepare_input(buf)
    output = run_model(input)
    return process_output(output,img_width,img_height)


def prepare_input(buf):
    img = Image.open(buf)
    img_width, img_height = img.size
    img = img.resize((640, 640))
    img = img.convert("RGB")
    input = np.array(img)
    input = input.transpose(2, 0, 1)
    input = input.reshape(1, 3, 640, 640) / 255.0
    return input.astype(np.float32), img_width, img_height


def detect_items(photo_name: str):
    results = model.predict(unprocessed_photo_folder+photo_name)
    result = results[0]
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [
            round(x) for x in box.xyxy[0].tolist()
        ]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        output.append([
            x1, y1, x2, y2, result.names[class_id], prob
        ])
    return output


def run_model(input):
    model = ort.InferenceSession("neuro_processing/detector.onnx")
    outputs = model.run(["output0"], {"images":input})
    return outputs[0]


def iou(box1,box2):
    return intersection(box1,box2)/union(box1,box2)


def union(box1,box2):
    box1_x1,box1_y1,box1_x2,box1_y2 = box1[:4]
    box2_x1,box2_y1,box2_x2,box2_y2 = box2[:4]
    box1_area = (box1_x2-box1_x1)*(box1_y2-box1_y1)
    box2_area = (box2_x2-box2_x1)*(box2_y2-box2_y1)
    return box1_area + box2_area - intersection(box1,box2)


def intersection(box1,box2):
    box1_x1,box1_y1,box1_x2,box1_y2 = box1[:4]
    box2_x1,box2_y1,box2_x2,box2_y2 = box2[:4]
    x1 = max(box1_x1,box2_x1)
    y1 = max(box1_y1,box2_y1)
    x2 = min(box1_x2,box2_x2)
    y2 = min(box1_y2,box2_y2)
    return (x2-x1)*(y2-y1)


def process_output(output, img_width, img_height):
    output = output[0].astype(float)
    output = output.transpose()

    boxes = []
    for row in output:
        prob = row[4:].max()
        if prob < 0.5:
            continue
        class_id = row[4:].argmax()
        label = yolo_classes[class_id]
        xc, yc, w, h = row[:4]
        x1 = (xc - w/2) / 640 * img_width
        y1 = (yc - h/2) / 640 * img_height
        x2 = (xc + w/2) / 640 * img_width
        y2 = (yc + h/2) / 640 * img_height
        boxes.append([x1, y1, x2, y2, label, prob])

    boxes.sort(key=lambda x: x[5], reverse=True)
    result = []
    while len(boxes) > 0:
        result.append(boxes[0])
        boxes = [box for box in boxes if iou(box, boxes[0]) < 0.7]
    return result


def draw_rectangles(photo_name: str, coordinates_list: list):
    image = Image.open(unprocessed_photo_folder + photo_name)
    font = ImageFont.truetype('./Font/Karla-VariableFont_wght.ttf', 60)
    for coords in coordinates_list:
        x, y, width, height, value, precision = coords
        text = f"value: {value} \n precision: {round(precision, 3)}"
        draw = ImageDraw.Draw(image)
        draw.rectangle((x, y, width, height), outline=(255, 0, 0), width=5)
        draw.text((x, y, width, height), text=text, fill=None, font=font, anchor=None, spacing=0, align="left")

    image.save(processed_photo_folder + photo_name)

    return processed_photo_folder + photo_name
