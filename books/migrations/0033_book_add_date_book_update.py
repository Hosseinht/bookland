# Generated by Django 4.1 on 2022-11-20 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0032_alter_book_options_alter_category_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="add_date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="update",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
