# Generated by Django 4.1 on 2022-11-28 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0043_alter_author_name_alter_book_cover_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="book",
            name="publisher",
            field=models.CharField(max_length=200),
        ),
    ]
