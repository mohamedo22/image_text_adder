from django.shortcuts import render
from django.http import HttpResponse
from .forms import TextForm
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO
import base64
import tempfile
from PIL import Image
from zipfile import ZipFile
def home(request):
    if request.method == 'POST':
        valueOfPath = request.POST['value-radio']
        form = TextForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data['text2'].split(',')
            names = [name.strip() for name in names if name.strip()]  

            texts = [form.cleaned_data[f'text{i}'] for i in range(1, 9)]
            image_paths = {
                "c1": 'image_editor/images/ce_1.jpg',
                "c2": 'image_editor/images/ce_2.jpg',
                "c3": 'image_editor/images/ce_3.jpg',
                "c4": 'image_editor/images/ce_4t.jpg',
                "c5": 'image_editor/images/ce_5t.jpg'
            }
            image_path = image_paths.get(valueOfPath, 'image_editor/images/default.jpeg')
            images_base64 = []
            counter = 0
            for name in names:
                image = Image.open(image_path)
                draw = ImageDraw.Draw(image)

                # Update the second text with the name
                texts[1] = name

                # Define positions, fonts, colors, and sizes for each text
                y_positions = [1000, 1200, 1400, 1700, 2100, 2300, 2100, 2300]
                fonts = [
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
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
                    (0, 131, 117),
                    (0, 0, 0),
                    (0, 131, 117),
                    (0, 0, 0),
                ] 
                image_width = image.width
                # Draw text on the image
                for i,(text, y_position, font, color) in enumerate(zip(texts, y_positions, fonts, colors)):
                    reshaped_text = arabic_reshaper.reshape(text)  # Reshape the text
                    bidi_text = get_display(reshaped_text)  # Handle bidirectional text
                    if i == len(texts) - 1 or i == len(texts) - 4:
                        x_position = 200
                    elif i == len(texts) - 2 or i == len(texts) - 3: 
                        x_position = 2300
                    else:
                        # Calculate text size using textbbox
                        text_bbox = draw.textbbox((0, 0), bidi_text, font=font)
                        text_width = text_bbox[2] - text_bbox[0]

                        # Calculate x position to center the text
                        x_centered = (image_width - text_width) // 2
                        x_position = x_centered
                    # Draw the text
                    draw.text((x_position, y_position), bidi_text, fill=color, font=font)

                response_image = BytesIO()
                image.save(response_image, 'JPEG')
                response_image.seek(0)
                image_base64 = base64.b64encode(response_image.getvalue()).decode('UTF-8')
                images_base64.append(image_base64)
                counter+=1
            request.session['images'] = images_base64
            request.session['names'] = names
            if counter != 0:
                first_image = image_base64[0]
            else:
                first_image = None 
            return render(request, 'pdf_template.html',  {'image': first_image, 'names': names})
    else:
        form = TextForm()
    return render(request, 'upload_image.html', {'form': form})
def download_pdf(request):
    images_base64 = request.session.get('images')
    names = request.session.get('names')
    if not images_base64 or not names:
        return HttpResponse('No images or names to download', status=400)
    
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
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{name}.pdf"'

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
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="all_pdfs.zip"'
    return response
def download_from_home(request):
    if request.method == 'POST':
        valueOfPath = request.POST['value-radio']
        form = TextForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data['text2'].split(',')
            names = [name.strip() for name in names if name.strip()]

            texts = [form.cleaned_data[f'text{i}'] for i in range(1, 9)]
            image_paths = {
                "c1": 'image_editor/images/ce_1.jpg',
                "c2": 'image_editor/images/ce_2.jpg',
                "c3": 'image_editor/images/ce_3.jpg',
                "c4": 'image_editor/images/ce_4t.jpg',
                "c5": 'image_editor/images/ce_5t.jpg'
            }
            image_path = image_paths.get(valueOfPath, 'image_editor/images/default.jpeg')
            images_base64 = []

            for name in names:
                image = Image.open(image_path)
                draw = ImageDraw.Draw(image)

                # Update the second text with the name
                texts[1] = name

                # Define positions, fonts, colors, and sizes for each text
                y_positions = [1000, 1200, 1400, 1700, 2100, 2300, 2100, 2300]
                fonts = [
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
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
                    if i == len(texts) - 1 or i == len(texts) - 4:
                        x_position = 200
                    elif i == len(texts) - 2 or i == len(texts) - 3:
                        x_position = 2300
                    else:
                        # Calculate text size using textbbox
                        text_bbox = draw.textbbox((0, 0), bidi_text, font=font)
                        text_width = text_bbox[2] - text_bbox[0]

                        # Calculate x position to center the text
                        x_centered = (image_width - text_width) // 2
                        x_position = x_centered
                    # Draw the text
                    draw.text((x_position, y_position), bidi_text, fill=color, font=font)

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
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="all_pdfs.zip"'
            return response

    else:
        form = TextForm()
        return render(request, 'upload_image.html', {'form': form})