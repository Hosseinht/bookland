# Generated by Django 4.1 on 2022-11-28 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0045_alter_book_publisher_alter_book_title_and_more"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="book",
            name="book_title_gin_index",
        ),
        migrations.AlterField(
            model_name="book",
            name="title",
            field=models.CharField(max_length=1000),
        ),
    ]