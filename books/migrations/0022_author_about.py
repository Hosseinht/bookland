# Generated by Django 4.1 on 2022-11-01 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0021_alter_category_options_rename_title_category_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="about",
            field=models.TextField(max_length=3000, null=True),
        ),
    ]
