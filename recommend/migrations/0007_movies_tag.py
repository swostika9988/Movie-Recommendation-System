# Generated by Django 5.0.6 on 2024-07-07 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0006_alter_movies_imdb_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='tag',
            field=models.CharField(choices=[('normal', 'normal'), ('popular', 'popular'), ('upcomming', 'upcomming'), ('top_rated', 'top_rated'), ('most_reviewd', 'most_reviewd')], default='normal', max_length=30),
        ),
    ]
