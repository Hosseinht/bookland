# Generated by Django 4.1 on 2022-08-22 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0004_alter_book_isbn"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="pseudonym",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
