# myapp/tasks.py
from celery import shared_task
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import base64
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from zipfile import ZipFile

@shared_task
def process_images(image_paths, names, texts):
    images_base64 = []
    for image_path, name in zip(image_paths, names):
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        texts[1] = name  # Update the second text with the name

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

        for i, (text, y_position, font, color) in enumerate(zip(texts, y_positions, fonts, colors)):
            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)
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
                    y_position += text_bbox[3] - text_bbox[1] + 10

        response_image = BytesIO()
        image.save(response_image, 'JPEG')
        response_image.seek(0)
        image_base64 = base64.b64encode(response_image.getvalue()).decode('UTF-8')
        images_base64.append(image_base64)

    pdf_buffers = []
    for image_base64, name in zip(images_base64, names):
        image_data = base64.b64decode(image_base64)
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(image_data)
            tmp_file.flush()
            tmp_file.close()
            image_path = tmp_file.name

        try:
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
            pdf_buffers.append(pdf)
        finally:
            pass

    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, 'w') as zf:
        for name, pdf in zip(names, pdf_buffers):
            zf.writestr(f'{name}.pdf', pdf)

    zip_buffer.seek(0)
    return base64.b64encode(zip_buffer.getvalue()).decode('utf-8')
