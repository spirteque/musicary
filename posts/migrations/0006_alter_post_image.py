# Generated by Django 4.2.5 on 2023-09-20 00:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0005_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(upload_to="posts_photos/%Y/%m/%d"),
        ),
    ]
