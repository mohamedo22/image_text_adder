from django.db import models
from django.contrib.auth.models import User 
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    CHOICES = [
        ('ce_1.jpeg', 'Image 1'),
        ('ce_2.jpeg', 'Image 2'),
        ('ce_3.jpeg', 'Image 3'),
        ('ce_4t.jpeg', 'Image 4'),
        ('ce_5t.jpeg', 'Image 5'),
    ]
    selected_image = models.CharField(max_length=50, choices=CHOICES)
    text1 = models.CharField(max_length=100)
    text2 = models.CharField(max_length=100)
    text3 = models.CharField(max_length=100)
    text4 = models.CharField(max_length=100)
    text5 = models.CharField(max_length=100)
    text6 = models.CharField(max_length=100)
    text7 = models.CharField(max_length=100)
    text8 = models.CharField(max_length=100)
    text9 = models.CharField(max_length=100)
    text10 = models.CharField(max_length=100)
class images(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    Shokr = models.ImageField(upload_to='images/' , default='images/ce_4.jpg')
    tahnqa = models.ImageField(upload_to='images/', default='images/ce_3.jpg')
    hodor = models.ImageField(upload_to='images/', default='images/ce_1.jpg')
    tafwoq = models.ImageField(upload_to='images/', default='images/ce_2.jpg')
class codes(models.Model):
    code = models.CharField(max_length=10000000 , null=True)
    active = models.BooleanField(default=True, null=True)
    type_code = models.CharField(max_length=50, null=True)
    amountOfUsers = models.PositiveIntegerField(default=0, null=True)
    date_of_creation = models.DateTimeField(auto_now_add=True, null=True)
    date_of_end = models.DateTimeField(null=True)
