# tasks.py

from celery import shared_task
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import base64
from io import BytesIO
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from django.http import HttpResponse
from zipfile import ZipFile

@shared_task
def generate_image(image_path, texts, name):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Update the second text with the name
    texts[1] = name

    # Define positions, fonts, colors, and sizes for each text
    y_positions = [1000, 1150, 1300, 1450, 1550, 1850, 2100, 2300, 2100, 2300]
    fonts = [
        ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
        ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 100),
        ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
        ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
        ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
        ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
        ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
        ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 75),
        ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
        ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 75),
    ]
    colors = [
        (0, 0, 0),
        (0, 131, 117),
        (0, 0, 0),
        (0, 0, 0),  
        (0, 0, 0),
        (0, 0, 0),
        (0, 131, 117),
        (0, 0, 0),
        (0, 131, 117),
        (0, 0, 0),
    ] 
    image_width = image.width

    # Draw text on the image
    for i, (text, y_position, font, color) in enumerate(zip(texts, y_positions, fonts, colors)):
        reshaped_text = arabic_reshaper.reshape(text)  # Reshape the text
        bidi_text = get_display(reshaped_text)  # Handle bidirectional text
        words = bidi_text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + ' ' + word
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            if text_width <= image_width - 400:  
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)

        if i == len(texts) - 1 or i == len(texts) - 4:
            for line in lines:
                x_position = 200
                draw.text((x_position, y_position), line, fill=color, font=font)
        elif i == len(texts) - 2 or i == len(texts) - 3:
            for line in lines:
                x_position = 2300
                draw.text((x_position, y_position), line, fill=color, font=font)
        else:
            for line in lines:
                text_bbox = draw.textbbox((0, 0), line, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                x_position = (image_width - text_width) // 2
                draw.text((x_position, y_position), line, fill=color, font=font)
                y_position += text_bbox[3] - text_bbox[1] + 10  # Move to next line position with some spacing

    response_image = BytesIO()
    image.save(response_image, 'JPEG')
    response_image.seek(0)
    image_base64 = base64.b64encode(response_image.getvalue()).decode('UTF-8')
    return image_base64

@shared_task
def generate_pdf(image_base64, name):
    image_data = base64.b64decode(image_base64)
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(image_data)
        tmp_file.flush()
        tmp_file.close()
        image_path = tmp_file.name

    image = Image.open(image_path)
    img = ImageReader(image_path)
    img_width, img_height = img.getSize()
    scaling_factor_width = letter[0] / img_width
    scaling_factor_height = letter[1] / img_height
    scaling_factor = min(scaling_factor_width, scaling_factor_height)
    new_width = img_width * scaling_factor * 0.9
    new_height = img_height * scaling_factor * 0.9

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(600, 430))
    p.drawImage(img, 0, 0, width=img_width * scaling_factor, height=img_height * scaling_factor, preserveAspectRatio=True, mask='auto')
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf