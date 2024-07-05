# Generated by Django 5.0.6 on 2024-07-05 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_editor', '0009_delete_codes'),
    ]

    operations = [
        migrations.CreateModel(
            name='codes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=1000)),
                ('active', models.BooleanField(default=True)),
                ('type_of_code', models.CharField(max_length=50)),
                ('data_of_creation', models.DateField(auto_now_add=True)),
                ('data_of_end', models.DateField()),
                ('amount_of_users', models.PositiveIntegerField()),
            ],
        ),
    ]
