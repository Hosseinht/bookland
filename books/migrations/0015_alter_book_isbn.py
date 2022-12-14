# Generated by Django 4.1 on 2022-08-27 06:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0014_remove_book_author_alter_review_rating_book_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="isbn",
            field=models.CharField(
                max_length=13,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9]*$", "ISBN contains numbers not words!"
                    ),
                    django.core.validators.MaxLengthValidator(13),
                ],
            ),
        ),
    ]
