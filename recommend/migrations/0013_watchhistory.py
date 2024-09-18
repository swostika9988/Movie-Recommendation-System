# Generated by Django 5.1 on 2024-09-18 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0012_alter_movies_tag_alter_trendingmovie_tag_reviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('count', models.IntegerField(default=1)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommend.movies')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommend.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
