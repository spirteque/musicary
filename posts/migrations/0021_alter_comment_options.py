# Generated by Django 4.2.5 on 2023-09-28 22:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0020_remove_comment_username_comment_username"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ("-created",)},
        ),
    ]
