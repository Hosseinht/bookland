# Generated by Django 4.1 on 2022-11-30 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0053_book_book_title_idx"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="book",
            name="book_title_idx",
        ),
    ]
