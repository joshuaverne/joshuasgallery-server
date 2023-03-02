# Generated by Django 4.1.5 on 2023-03-02 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_gallerypiece_description_alter_gallerypiece_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallerypiece',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='gallerypiece',
            name='galleries',
            field=models.ManyToManyField(blank=True, to='gallery.exhibition'),
        ),
        migrations.AlterField(
            model_name='gallerypiece',
            name='title',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
