# Generated by Django 4.2.5 on 2023-10-06 23:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_remove_profile_id_alter_profile_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="photo",
        ),
        migrations.AddField(
            model_name="profile",
            name="image",
            field=models.ImageField(blank=True, upload_to="profile_images/%Y/%m/%d"),
        ),
    ]