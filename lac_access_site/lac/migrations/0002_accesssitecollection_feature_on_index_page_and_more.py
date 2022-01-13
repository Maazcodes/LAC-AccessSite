# Generated by Django 4.0 on 2022-01-13 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesssitecollection',
            name='feature_on_index_page',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='accesssitecollection',
            name='image',
            field=models.ImageField(default='canada.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='accesssitecollection',
            name='description_en',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='accesssitecollection',
            name='description_fr',
            field=models.TextField(),
        ),
    ]
