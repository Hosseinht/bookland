# Generated by Django 4.1 on 2022-11-28 14:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0046_remove_book_book_title_gin_index_alter_book_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="isbn",
            field=models.CharField(
                max_length=13,
                validators=[django.core.validators.MaxLengthValidator(13)],
            ),
        ),
    ]
