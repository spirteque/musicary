# Generated by Django 4.2.5 on 2023-09-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0014_alter_post_friend_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="artists",
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name="post",
            name="genre",
            field=models.CharField(max_length=400),
        ),
    ]