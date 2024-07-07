# Generated by Django 5.0.6 on 2024-07-07 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=100)),
                ('poster_url', models.CharField(blank=True, max_length=300, null=True)),
                ('trailer_url', models.CharField(blank=True, max_length=300, null=True)),
                ('actors', models.CharField(blank=True, max_length=300, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('rating', models.FloatField(default=0)),
                ('poster_path', models.CharField(blank=True, max_length=300, null=True)),
                ('adult', models.BooleanField(default=False)),
                ('budget', models.FloatField(default=0)),
                ('homepage', models.CharField(blank=True, max_length=300, null=True)),
                ('imdb_id', models.IntegerField(blank=True, null=True)),
                ('popularity', models.FloatField(default=0)),
                ('revenue', models.FloatField(default=0)),
                ('runtime', models.IntegerField(default=0)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('tagline', models.CharField(blank=True, max_length=200, null=True)),
                ('vote_count', models.FloatField(default=0)),
                ('vote_average', models.FloatField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]