# Generated by Django 5.0.6 on 2024-07-07 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0004_remove_movies_geners_movies_geners'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movies',
            old_name='geners',
            new_name='genres',
        ),
    ]