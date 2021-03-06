# Generated by Django 2.2 on 2019-06-09 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('stock', models.IntegerField()),
                ('feature_1', models.CharField(blank=True, max_length=220, null=True)),
                ('feature_2', models.CharField(blank=True, max_length=220, null=True)),
                ('feature_3', models.CharField(blank=True, max_length=220, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
