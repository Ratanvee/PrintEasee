# Generated by Django 4.2.19 on 2025-02-24 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_document_uploaded_by_document_color_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='num_pages',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='document',
            name='color_type',
            field=models.CharField(choices=[('color', 'Color'), ('bw', 'Black & White')], max_length=10),
        ),
        migrations.AlterField(
            model_name='document',
            name='paper_size',
            field=models.CharField(choices=[('A4', 'A4'), ('A3', 'A3')], default='A4', max_length=10),
        ),
    ]
