# Generated by Django 4.1 on 2022-11-28 17:32

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0048_alter_book_title_book_newginindex"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="book",
            name="NewGinIndex",
        ),
        migrations.AddIndex(
            model_name="book",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["title", "description"], name="NewGinIndex"
            ),
        ),
    ]