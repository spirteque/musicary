# Generated by Django 4.2.5 on 2023-09-28 17:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0018_alter_post_friend_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="audio",
            field=models.URLField(blank=True, null=True),
        ),
    ]