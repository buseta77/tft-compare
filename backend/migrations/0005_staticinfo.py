# Generated by Django 4.1 on 2022-08-24 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_matchinfo_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=999999)),
                ('info', models.CharField(max_length=50)),
            ],
        ),
    ]
