# Generated by Django 4.1 on 2022-11-29 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0049_remove_book_newginindex_book_newginindex"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="name",
            field=models.CharField(max_length=1000),
        ),
    ]
