from celery import shared_task
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
import zipfile

@shared_task
def process_images(image_paths, names, texts):
    images_base64 = []
    for name, image_path in zip(names, image_paths):
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        
        texts[1] = name
        
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
            draw.text((200, y_position), text, fill=color, font=font)
        
        response_image = BytesIO()
        image.save(response_image, 'JPEG')
        response_image.seek(0)
        image_base64 = base64.b64encode(response_image.getvalue()).decode('UTF-8')
        images_base64.append(image_base64)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        for name, image_base64 in zip(names, images_base64):
            image_data = base64.b64decode(image_base64)
            zf.writestr(f'{name}.jpg', image_data)

    zip_buffer.seek(0)
    zip_data = base64.b64encode(zip_buffer.getvalue()).decode('utf-8')
    return zip_data
