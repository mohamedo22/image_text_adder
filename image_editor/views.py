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
from django.http import JsonResponse
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
        codes_ = codes(user = user , monthCode="jdikd2" , yearCode = "owwekdds5")
        codes_()
    if request.method == 'POST':
        valueOfPath = request.POST['value-radio']
        pass_code = request.POST.get('passCode')
        codes_ = codes.objects.get(user__username ='Ayman Ahmed')
        if pass_code == codes_.monthCode:
            codes_.amountOfMonthUsers+=1
        elif pass_code == codes_.yearCode:
            codes_.amountOfYearUsers+=1
        codes_.save()
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
            draw = ImageDraw.Draw(image)
            
            texts[1] = first_name  # Use only the first name here

            y_positions = [800, 950, 1200, 1400, 1550, 1700, 2000, 2150, 2000, 2150]
            fonts = [
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 150),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
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

                if i == len(texts) - 4:
                    for line in lines:
                        x_position = 200
                        draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 3 :
                    for line in lines:
                        x_position = 250
                        draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 2 :
                    for line in lines:
                        x_position = 2700
                        draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 1:
                    for line in lines:
                        x_position = 2750
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
            image.save(response_image, format=image_format)
            response_image.seek(0)
            image_base64 = base64.b64encode(response_image.getvalue()).decode('UTF-8')
            images_base64.append(image_base64)

            request.session['images'] = images_base64
            request.session['names'] = [first_name]

            return render(request, 'pdf_template.html', {'image': images_base64[0], 'names': [first_name]})
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
        check = User.objects.filter(username="Ayman Ahmed" , password="Ayman Ahmed@123").first
        if check:
            pass
    except:
        user = User.objects.create(username="Ayman Ahmed" , password="Ayman Ahmed@123")
        user.save()
        images_of_cer = images(user = user )
        images_of_cer.save()
        codes_ = codes(user = user , monthCode="jdikd2" , yearCode = "owwekdds5")
        codes_.save()
    if request.method == 'POST':
        valueOfPath = request.POST['value-radio']
        pass_code = request.POST.get('passCode')
        codes_ = codes.objects.get(user__username ='Ayman Ahmed')
        if pass_code == codes_.monthCode:
            codes_.amountOfMonthUsers+=1
        elif pass_code == codes_.yearCode:
            codes_.amountOfYearUsers+=1
        codes_.save()
        form = TextForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data['text2'].replace('\r\n', '\n').split('\n')
            names = [name.strip() for name in names if name.strip()]  
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
            counter = 0
            for name in names:
                image = Image.open(image_path)
                draw = ImageDraw.Draw(image)

                # Update the second text with the name
                texts[1] = name

                # Define positions, fonts, colors, and sizes for each text
                y_positions = [800, 950, 1200, 1400, 1550, 1700, 2000, 2150, 2000, 2150]
                fonts = [
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 150),
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

                    if i == len(texts) - 4:
                        for line in lines:
                            x_position = 200
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 3 :
                        for line in lines:
                            x_position = 250
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 2 :
                        for line in lines:
                            x_position = 2700
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 1:
                        for line in lines:
                            x_position = 2750
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
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="all_pdfs.zip"'
            
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
        codes_ = codes(user = user , monthCode="jdikd2" , yearCode = "owwekdds5")
        codes_()
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
            draw = ImageDraw.Draw(image)
            
            texts[1] = first_name 
            
            y_positions = [800, 950, 1200, 1400, 1550, 1700, 2000, 2150, 2000, 2150,500]
            fonts = [
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 150),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 80),
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
            image_width = image.width

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
                        current_line = word

                lines.append(current_line)

                if i == len(texts) - 5:
                    for line in lines:
                        x_position = 200
                        draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 4 :
                    for line in lines:
                        x_position = 250
                        draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 3 :
                    for line in lines:
                        x_position = 2700
                        draw.text((x_position, y_position), line, fill=color, font=font)
                elif i == len(texts) - 2:
                    for line in lines:
                        x_position = 2750
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
            image.save(response_image, format=image_format)
            response_image.seek(0)
            image_base64 = base64.b64encode(response_image.getvalue()).decode('UTF-8')
            images_base64.append(image_base64)

            request.session['images'] = images_base64
            request.session['names'] = [first_name]

            return render(request, 'pdf_template.html', {'image': images_base64[0], 'names': [first_name]})
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
        codes_ = codes(user = user , monthCode="jdikd2" , yearCode = "owwekdds5")
        codes_.save()
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
                "c2": 'media/images/thnqaFree.jpg',
                "c1": 'media/images/shqrFree.jpg',
            }
            image_path = image_paths.get(valueOfPath, 'image_editor/images/default.jpeg')
            images_base64 = []
            counter = 0
            for name in names:
                image = Image.open(image_path)
                draw = ImageDraw.Draw(image)

                texts[1] = name

                y_positions = [800, 950, 1200, 1400, 1550, 1700, 2000, 2150, 2000, 2150,500]
                fonts = [
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 150),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 70),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 75),
                    ImageFont.truetype("image_editor/fonts/araib/second_font.ttf", 90),
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

                    if i == len(texts) - 5:
                        for line in lines:
                            x_position = 200
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 4 :
                        for line in lines:
                            x_position = 250
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 3 :
                        for line in lines:
                            x_position = 2700
                            draw.text((x_position, y_position), line, fill=color, font=font)
                    elif i == len(texts) - 2:
                        for line in lines:
                            x_position = 2750
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
        codes_ = codes(user=user, monthCode="jdikd2", yearCode="owwekdds5")
        codes_.save()

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
    codes_ = codes.objects.get(user = user)
    context = {
        'images':images_,
        'codes':codes_
    }
    return render(request , 'adminHome.html' , context)
def change_codes(request):
    if request.method == 'POST':
        codes_ = codes.objects.get(user=request.user)
        yearCode = request.POST['yearCode']
        activeYear = request.POST.get('activeYear')
        monthCode = request.POST['monthCode']
        activeMonth = request.POST.get('activeMonth')
        activeYear = True if activeYear == 'on' else False
        activeMonth = True if activeMonth == 'on' else False

        codes_.monthCode = monthCode
        codes_.yearCode = yearCode
        codes_.yearActive = activeYear
        codes_.monthActive = activeMonth
        codes_.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
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
    code = request.GET.get('code')
    print(code)
    codes_ = codes.objects.get(user__username ='Ayman Ahmed')
    data = {'valid':False}
    if codes_.monthActive:
        if codes_.monthCode == code: 
            data['valid'] = True
    if codes_.yearActive:
        if codes_.yearCode == code:
            data['valid'] = True
    codes_.save()
    return JsonResponse(data)
