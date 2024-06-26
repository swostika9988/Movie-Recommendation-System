# Generated by Django 5.0.6 on 2024-06-22 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
