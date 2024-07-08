from django.shortcuts import render , redirect
from django.contrib.auth import login as auth_login
from django.core.exceptions import ObjectDoesNotExist
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
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from datetime import datetime, timedelta
from PyPDF2 import PdfMerger
def home(request):
    try:
        check = User.objects.filter(username="Ayman Ahmed" , password="Ayman Ahmed@123").first
        if check:
            pass
    except:
        user = User.objects.create(username="Ayman Ahmed" , password="Ayman Ahmed@123")
        user.save()
        images_of_cer = images(user = user )
        images_of_cer.save()
    if request.method == 'POST':
        valueOfPath = request.POST['value-radio']
        pass_code = request.POST.get('passCode')
        code_ = codes.objects.get(code = pass_code)
        if not request.session.get(f'c_{pass_code}',False):
                code_.amountOfUsers += 1
                request.session[f'c_{pass_code}'] = True
        code_.save()
        form = TextForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data['text2'].replace('\r\n', '\n').split('\n')
            names = [name.strip() for name in names if name.strip()]
            if names:
                first_name = names[0]
            else:
                first_name = "No Name Provided"

            texts = [form.cleaned_data[f'text{i}'] for i in range(1, 11)]
            images_= images.objects.get(user__username = "Ayman Ahmed")
            image_paths = {
                "c4": images_.tafwoq,
                "c3": images_.hodor,
                "c2": images_.tahnqa,
                "c1": images_.Shokr,
            }
            image_path = image_paths.get(valueOfPath, 'image_editor/images/default.jpeg')
            images_base64 = []
            image = Image.open(image_path)
            new_size = (3514, 2478)
            resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(resized_image)
            texts[1] = first_name  # Use only the first name here

            y_positions = [800, 950, 1200, 1400, 1550, 1700, 2000, 2150, 2000, 2150]
            fonts = [
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 150),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 100),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 85),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 100),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 85),
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
            image_width = resized_image.width

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
                        y_positions[i+1]+=100
                        y_positions[i+2] = y_positions[i+1]+100
                        current_line = word

                lines.append(current_line)

                def get_text_width(text, font):
                        text_bbox = draw.textbbox((0, 0), text, font=font)
                        return (text_bbox[2] - text_bbox[0])
                if i == len(texts) - 4:
                        for line in lines:
                            container_width = get_text_width(texts[len(texts) - 3], fonts[len(texts) - 3])
                            text_width = get_text_width(line, font)
                            x_position = (container_width - text_width) // 2 + 400
                            draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 3 :
                        for line in lines:
                            x_position = 400
                            draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 2 :
                        for line in lines:
                            container_width = get_text_width(texts[len(texts) - 1], fonts[len(texts) - 1])
                            text_width = get_text_width(line, font)
                            x_position = (container_width - text_width) // 2 + 2400
                            draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 1:
                        for line in lines:
                            x_position = 2500
                            draw.text((x_position, y_position), line, fill=color, font=font)
                else:
                    for line in lines:
                        text_bbox = draw.textbbox((0, 0), line, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        x_position = (image_width - text_width) // 2
                        draw.text((x_position, y_position), line, fill=color, font=font)
                        y_position += text_bbox[3] - text_bbox[1] + 10 

            response_image = BytesIO()
            image_format = image.format
            resized_image.save(response_image, format=image_format)
            response_image.seek(0)
            image_base64 = base64.b64encode(response_image.getvalue()).decode('UTF-8')
            images_base64.append(image_base64)

            request.session['images'] = images_base64
            request.session['names'] = [first_name]
            image_data = base64.b64decode(images_base64[0])
            # return render(request, 'pdf_template.html', {'image': images_base64[0], 'names': [first_name]})
            return HttpResponse(image_data , content_type='image/jpeg')
    else:
        form = TextForm()
    return render(request, 'upload_image.html', {'form': form})
# def download_pdf(request):
#     images_base64 = request.session.get('images')
#     names = request.session.get('names')
#     if not images_base64 or not names:
#         return HttpResponse('No images or names to download', status=400)
    
#     pdf_buffers = []
    
#     for image_base64, name in zip(images_base64, names):
#         image_data = base64.b64decode(image_base64)
        
#         with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#             tmp_file.write(image_data)
#             tmp_file.flush()
#             tmp_file.close()
#             image_path = tmp_file.name
        
#         try:
#             image = Image.open(image_path)
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename="{name}.pdf"'

#             img = ImageReader(image_path)
#             img_width, img_height = img.getSize()
#             scaling_factor_width = letter[0] / img_width
#             scaling_factor_height = letter[1] / img_height
#             scaling_factor = min(scaling_factor_width, scaling_factor_height)
#             new_width = img_width * scaling_factor * 0.9
#             new_height = img_height * scaling_factor * 0.9

#             buffer = BytesIO()
#             p = canvas.Canvas(buffer, pagesize=(600, 430))
#             p.drawImage(img, 0, 0, width=img_width * scaling_factor, height=img_height * scaling_factor, preserveAspectRatio=True, mask='auto')
#             p.showPage()
#             p.save()
            
#             pdf = buffer.getvalue()
#             buffer.close()
#             pdf_buffers.append(pdf)
#         finally:
#             pass
    
#     zip_buffer = BytesIO()
#     with ZipFile(zip_buffer, 'w') as zf:
#         for name, pdf in zip(names, pdf_buffers):
#             zf.writestr(f'{name}.pdf', pdf)
    
#     zip_buffer.seek(0)
#     response = HttpResponse(zip_buffer, content_type='application/zip')
#     response['Content-Disposition'] = 'attachment; filename="all_pdfs.zip"'
#     return response
def download_from_home(request):
    try:
        check = User.objects.filter(username="Ayman Ahmed", password="Ayman Ahmed@123").first()
        if not check:
            raise User.DoesNotExist
    except User.DoesNotExist:
        user = User.objects.create(username="Ayman Ahmed", password="Ayman Ahmed@123")
        user.save()
        images_of_cer = images(user=user)
        images_of_cer.save()

    if request.method == 'POST':
        valueOfPath = request.POST['value-radio']
        pass_code = request.POST.get('passCode')
        code_ = codes.objects.get(code=pass_code)
        if code_.type_code == 'month':
            if not request.session.get('month', False):
                request.session['month'] = True
                code_.amountOfUsers += 1
        elif code_.type_code == 'year':
            if not request.session.get('year', False):
                request.session['year'] = True
                code_.amountOfUsers += 1
        code_.save()
        form = TextForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data['text2'].replace('\r\n', '\n').split('\n')
            names = [name.strip() for name in names if name.strip()]  
            texts = [form.cleaned_data[f'text{i}'] for i in range(1, 11)]
            images_ = images.objects.get(user__username="Ayman Ahmed")
            image_paths = {
                "c4": images_.tafwoq,
                "c3": images_.hodor,
                "c2": images_.tahnqa,
                "c1": images_.Shokr,
            }
            image_path = image_paths.get(valueOfPath, 'image_editor/images/default.jpeg')

            pdf_merger = PdfMerger()

            for name in names:
                image = Image.open(image_path)
                new_size = (3514, 2478)
                resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
                draw = ImageDraw.Draw(resized_image)

                # Clear the area for the second text (texts[1]) before drawing the new name
                clear_box_y_position = 950
                clear_box_height = 150
                draw.rectangle(
                    [0, clear_box_y_position, resized_image.width, clear_box_y_position + clear_box_height],
                    fill=(255, 255, 255)  # Assuming the background is white
                )

                # Update the second text with the name
                texts[1] = name

                # Define positions, fonts, colors, and sizes for each text
                y_positions = [800, 950, 1200, 1400, 1550, 1700, 2000, 2150, 2000, 2150]
                fonts = [
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 150),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 85),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 75),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 85),
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
                image_width = resized_image.width

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
                            y_positions[i+1] += 100
                            y_positions[i+2] = y_positions[i+1] + 100
                            current_line = word

                    lines.append(current_line)

                    def get_text_width(text, font):
                        text_bbox = draw.textbbox((0, 0), text, font=font)
                        return text_bbox[2] - text_bbox[0]

                    if i == len(texts) - 4:
                        for line in lines:
                            container_width = get_text_width(texts[len(texts) - 3], fonts[len(texts) - 3])
                            text_width = get_text_width(line, font)
                            x_position = (container_width - text_width) // 2 + 150
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 3:
                        for line in lines:
                            x_position = 200
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 2:
                        for line in lines:
                            container_width = get_text_width(texts[len(texts) - 1], fonts[len(texts) - 1])
                            text_width = get_text_width(line, font)
                            x_position = (container_width - text_width) // 2 + 2650
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 1:
                        for line in lines:
                            x_position = 2700
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    else:
                        for line in lines:
                            text_bbox = draw.textbbox((0, 0), line, font=font)
                            text_width = text_bbox[2] - text_bbox[0]
                            x_position = (image_width - text_width) // 2
                            draw.text((x_position, y_position), line, fill=color, font=font)
                            y_position += text_bbox[3] - text_bbox[1] + 10

                response_image = BytesIO()
                resized_image.save(response_image, 'JPEG')
                response_image.seek(0)
                image_base64 = base64.b64encode(response_image.getvalue()).decode('UTF-8')
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

                pdf_merger.append(BytesIO(pdf))

            merged_pdf_buffer = BytesIO()
            pdf_merger.write(merged_pdf_buffer)
            pdf_merger.close()
            merged_pdf_buffer.seek(0)

            response = HttpResponse(merged_pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="الشهادات.pdf"'
            return response

    else:
        form = TextForm()
        return render(request, 'upload_image.html', {'form': form})
def homeTagreba(request):
    try:
        check = User.objects.filter(username="Ayman Ahmed" , password="Ayman Ahmed@123").first
        if check:
            pass
    except:
        user = User.objects.create(username="Ayman Ahmed" , password="Ayman Ahmed@123")
        user.save()
        images_of_cer = images(user = user )
        images_of_cer.save()
    if request.method == 'POST':
        valueOfPath = request.POST['value-radio']
        form = TextForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data['text2'].replace('\r\n', '\n').split('\n')
            names = [name.strip() for name in names if name.strip()]
            if names:
                first_name = names[0]
            else:
                first_name = "No Name Provided"

            texts = [form.cleaned_data[f'text{i}'] for i in range(1, 11)]
            texts.append('**منتج خدمة تجريبية ')
            images_= images.objects.get(user__username = "Ayman Ahmed")
            image_paths = {
                "c1": images_.Shokr,
                "c2": images_.tahnqa,
            }
            image_path = image_paths.get(valueOfPath, 'image_editor/images/default.jpeg')
            images_base64 = []

            image = Image.open(image_path)
            new_size = (3514, 2478)
            resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(resized_image)
            
            texts[1] = first_name 
            
            y_positions = [800, 950, 1200, 1400, 1550, 1700, 2000, 2150, 2000, 2150,500]
            fonts = [
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 150),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 100),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 85),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 100),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 85),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
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
                (230,0,0),
            ] 
            image_width = resized_image.width

            # Draw text on the image
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
                        y_positions[i+1]+=100
                        y_positions[i+2] = y_positions[i+1]+100
                        current_line = word

                lines.append(current_line)
                def get_text_width(text, font):
                    text_bbox = draw.textbbox((0, 0), text, font=font)
                    return text_bbox[2] - text_bbox[0]
                if i == len(texts) - 5:
                    for line in lines:
                        container_width = get_text_width(texts[len(texts) - 4], fonts[len(texts) - 4])
                        text_width = get_text_width(line, font)
                        x_position = (container_width - text_width) // 2 + 350
                        draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 4 :
                    for line in lines:
                        x_position = 400
                        draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 3 :
                    for line in lines:
                        container_width = get_text_width(texts[len(texts) - 2], fonts[len(texts) - 2])
                        text_width = get_text_width(line, font)
                        x_position = (container_width - text_width) // 2 + 2400
                        draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 2:
                    for line in lines:
                        x_position = 2500
                        draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 1:
                    for line in lines:
                        x_position = 2900
                        draw.text((x_position, y_position), line, fill=color, font=font)
                else:
                    for line in lines:
                        text_bbox = draw.textbbox((0, 0), line, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        x_position = (image_width - text_width) // 2
                        draw.text((x_position, y_position), line, fill=color, font=font)
                        y_position += text_bbox[3] - text_bbox[1] + 10  # Move to next line position with some spacing

            response_image = BytesIO()
            image_format = image.format
            resized_image.save(response_image, format=image_format)
            response_image.seek(0)
            image_base64 = base64.b64encode(response_image.getvalue()).decode('UTF-8')
            images_base64.append(image_base64)

            request.session['images'] = images_base64
            request.session['names'] = [first_name]

            # return render(request, 'pdf_template.html', {'image': images_base64[0], 'names': [first_name]})
            image_data = base64.b64decode(images_base64[0])
            return HttpResponse(image_data , content_type = 'image/jpeg')
    form = TextForm()
    return render(request, 'tgreba.html', {'form': form})
def download_from_homeTagreba(request):
    try:
        check = User.objects.filter(username="Ayman Ahmed" , password="Ayman Ahmed@123").first
        if check:
            pass
    except:
        user = User.objects.create(username="Ayman Ahmed" , password="Ayman Ahmed@123")
        user.save()
        images_of_cer = images(user = user )
        images_of_cer.save()
    if request.method == 'POST':
        valueOfPath = request.POST['value-radio']
        form = TextForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data['text2'].replace('\r\n', '\n').split('\n')
            names = [name.strip() for name in names if name.strip()]  
            texts = [form.cleaned_data[f'text{i}'] for i in range(1, 11)]
            texts.append('**منتج خدمة تجريبية ')
            images_= images.objects.get(user__username = "Ayman Ahmed")
            image_paths = {
                "c2": images_.tahnqa,
                "c1": images_.Shokr,
            }
            image_path = image_paths.get(valueOfPath, 'image_editor/images/default.jpeg')
            images_base64 = []
            counter = 0
            for name in names:
                image = Image.open(image_path)
                new_size = (3514, 2478)
                resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
                draw = ImageDraw.Draw(resized_image)

                texts[1] = name

                y_positions = [800, 950, 1200, 1400, 1550, 1700, 2000, 2150, 2000, 2150,500]
                fonts = [
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 150),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 85),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 75),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 85),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 75),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
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
                    (230,0,0)
                ] 
                image_width = resized_image.width

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
                            y_positions[i+1]+=100
                            y_positions[i+2] = y_positions[i+1]+100
                            current_line = word

                    lines.append(current_line)

                    def get_text_width(text, font):
                        text_bbox = draw.textbbox((0, 0), text, font=font)
                        return text_bbox[2] - text_bbox[0]
                    if i == len(texts) - 5:
                        for line in lines:
                            container_width = get_text_width(texts[len(texts) - 4], fonts[len(texts) - 4])
                            text_width = get_text_width(line, font)
                            x_position = (container_width - text_width) // 2 + 150
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 4 :
                        for line in lines:
                            x_position = 200
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 3 :
                        for line in lines:
                            container_width = get_text_width(texts[len(texts) - 2], fonts[len(texts) - 2])
                            text_width = get_text_width(line, font)
                            x_position = (container_width - text_width) // 2 + 2650
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 2:
                        for line in lines:
                            x_position = 2700
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 1:
                        for line in lines:
                            x_position = 2800
                            draw.text((x_position, y_position), line, fill=color, font=font)
                                

                    else:
                        for line in lines:
                            text_bbox = draw.textbbox((0, 0), line, font=font)
                            text_width = text_bbox[2] - text_bbox[0]
                            x_position = (image_width - text_width) // 2
                            draw.text((x_position, y_position), line, fill=color, font=font)
                            y_position += text_bbox[3] - text_bbox[1] + 10  # Move to next line position with some spacing

                response_image = BytesIO()
                resized_image.save(response_image, 'JPEG')
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
                    p = canvas.Canvas(buffer, pagesize=(600, 320))
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
        return render(request, 'tgreba.html', {'form': form})
def loginAdmin(request):
    try:
        check = User.objects.get(username="Ayman Ahmed")
    except User.DoesNotExist:
        user = User.objects.create(username="Ayman Ahmed", password="Ayman Ahmed@123")
        user.save()
        images_of_cer = images(user=user)
        images_of_cer.save()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            check = User.objects.get(username=username, password=password)
            auth_login(request, user=check)
            return redirect(adminHome)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': "خطأ في تسجيل الدخول"})

    return render(request, 'login.html')
@login_required
def adminHome(request):
    user = request.user
    images_ = images.objects.get(user = user)
    queryset = codes.objects.order_by('date_of_creation')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        codes_ = paginator.page(page)
    except PageNotAnInteger:
        codes_ = paginator.page(1)
    except EmptyPage:
        codes_ = paginator.page(paginator.num_pages)
    
    amount_of_year_users = 0
    amount_of_month_users = 0
    codesForCount = codes.objects.all()
    for code in codesForCount:
        if code.type_code == 'month':
            amount_of_month_users += code.amountOfUsers
        else:
            amount_of_year_users += code.amountOfUsers
    print(amount_of_month_users)
    print(amount_of_year_users)
    context = {
        'images': images_,
        'codes': codes_,
        'amountOfYearUsers': amount_of_year_users,
        'amountOfMonthUsers': amount_of_month_users,
    }
    return render(request, 'adminHome.html', context)
def change_codes(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        code_text = request.POST.get('code')
        active = request.POST.get('active')
        code = codes.objects.get(pk = pk)
        code.code = code_text
        code.active = True if active == 'on' else False
        code.save()
        return redirect(adminHome)
    return HttpResponse(status=204)
def delete_code(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        code = codes.objects.get(pk = pk)
        code.delete()
        return redirect(adminHome)
    return HttpResponse(status=204)
def change_images(request):
    if request.method == 'POST':
        images_ = images.objects.get(user=request.user)
        shoqr = request.FILES.get('shoqr')
        thnqa = request.FILES.get('thnqa')
        hodor = request.FILES.get('hodor')
        tafwaq = request.FILES.get('tafwaq')
        if shoqr is not None:
            images_.Shokr = shoqr
        if thnqa is not None:
            images_.tahnqa = thnqa
        if hodor is not None:
            images_.hodor = hodor
        if tafwaq is not None:
            images_.tafwoq = tafwaq
        images_.save()
        return redirect(adminHome)
    return HttpResponse(status=204)
def check_code(request):
    code_ = request.GET.get('code')
    data = {'valid':False}
    try:
        check = codes.objects.filter(code = code_).first()
        if check:
            now_date = datetime.now().date()
            if now_date < check.date_of_end.date() :
                if check.active:
                    data['valid'] = True
                else:
                    print("code not active")
            else:
                print('code is expired ')
        else:
            print('code not found')
    except AttributeError as e:
        print(f"AttributeError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return JsonResponse(data)
def create_code(request):
    if request.method == 'POST':
        code_text = request.POST.get('code')
        value_radio = request.POST.get('value-radio')
        if value_radio == 'month':
            code_creation = codes(code = code_text , type_code = 'month' )
            code_creation.date_of_end = datetime.now() + timedelta(days=30)
        elif value_radio == 'year':
            code_creation = codes(code = code_text , type_code = 'year' )
            code_creation.date_of_end = datetime.now() + timedelta(days=365)
        code_creation.save()
        return redirect(adminHome)
    return HttpResponse(status=204)
