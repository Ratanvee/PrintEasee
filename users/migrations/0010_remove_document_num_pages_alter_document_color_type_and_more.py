# Generated by Django 4.2.19 on 2025-02-24 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_document_num_pages_alter_document_color_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='num_pages',
        ),
        migrations.AlterField(
            model_name='document',
            name='color_type',
            field=models.CharField(choices=[('black_white', 'Black & White'), ('color', 'Color'), ('both', 'Both')], default='black_white', max_length=11),
        ),
        migrations.AlterField(
            model_name='document',
            name='paper_size',
            field=models.CharField(choices=[('A4', 'A4'), ('A3', 'A3'), ('Letter', 'Letter'), ('Legal', 'Legal')], default='A4', max_length=10),
        ),
    ]
