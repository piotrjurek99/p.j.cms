# Generated by Django 3.0.14 on 2021-11-16 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PJArticles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Tytuł wpisu')),
                ('description', models.CharField(max_length=100, verbose_name='Opis artykułu')),
                ('content', models.TextField(verbose_name='Tytuł wpisu')),
                ('pub_data', models.DateTimeField(auto_now_add=True, verbose_name='Data Publikacji')),
                ('pub_user', models.CharField(max_length=2, verbose_name='Publikował - Inicjały')),
            ],
        ),
    ]