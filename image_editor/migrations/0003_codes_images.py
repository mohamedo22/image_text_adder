# Generated by Django 5.0.6 on 2024-06-29 18:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_editor', '0002_alter_uploadedimage_selected_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='codes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthCode', models.CharField(max_length=10000000)),
                ('yearCode', models.CharField(max_length=10000000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(default='ce_1.jpg', upload_to='images/')),
                ('image2', models.ImageField(default='ce_2.jpg', upload_to='images/')),
                ('image3', models.ImageField(default='ce_3.jpg', upload_to='images/')),
                ('image4', models.ImageField(default='ce_4.jpg', upload_to='images/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]