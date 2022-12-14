# Generated by Django 4.1 on 2022-08-27 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0015_alter_book_isbn"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.IntegerField(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                default=5,
                max_length=1,
            ),
        ),
    ]
