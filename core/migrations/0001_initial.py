# Generated by Django 4.1.2 on 2022-10-24 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('scope_content_description', models.CharField(max_length=200)),
                ('citable_reference', models.CharField(max_length=200)),
            ],
        ),
    ]