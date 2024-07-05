# Generated by Django 5.0.6 on 2024-07-05 09:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_editor', '0007_alter_images_shokr_alter_images_hodor_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='codes',
            old_name='monthActive',
            new_name='active',
        ),
        migrations.RemoveField(
            model_name='codes',
            name='amountOfMonthUsers',
        ),
        migrations.RemoveField(
            model_name='codes',
            name='amountOfYearUsers',
        ),
        migrations.RemoveField(
            model_name='codes',
            name='monthCode',
        ),
        migrations.RemoveField(
            model_name='codes',
            name='user',
        ),
        migrations.RemoveField(
            model_name='codes',
            name='yearActive',
        ),
        migrations.RemoveField(
            model_name='codes',
            name='yearCode',
        ),
        migrations.AddField(
            model_name='codes',
            name='amount_of_users',
            field=models.PositiveIntegerField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codes',
            name='code',
            field=models.CharField(default='kmoskdslkds', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codes',
            name='data_of_creation',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codes',
            name='data_of_end',
            field=models.DateField(default='2024-7-5'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codes',
            name='type_of_code',
            field=models.CharField(default='month', max_length=50),
            preserve_default=False,
        ),
    ]