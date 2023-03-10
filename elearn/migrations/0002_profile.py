# Generated by Django 4.1.3 on 2023-02-10 04:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='images/')),
                ('first_name', models.CharField(default='', max_length=255)),
                ('last_name', models.CharField(default='', max_length=255)),
                ('email', models.EmailField(default='none@email.com', max_length=254)),
                ('birth_date', models.DateField(default='1975-12-12')),
                ('bio', models.TextField(default='')),
                ('city', models.CharField(default='', max_length=255)),
                ('state', models.CharField(default='', max_length=255)),
                ('country', models.CharField(default='', max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
