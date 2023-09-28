# Generated by Django 4.2.5 on 2023-09-28 10:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0012_alter_post_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="friend_tags",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="tagged_users",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]