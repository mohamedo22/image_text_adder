from django.db import models

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
