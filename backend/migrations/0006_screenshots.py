# Generated by Django 4.1 on 2022-09-05 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_staticinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screenshots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
    ]