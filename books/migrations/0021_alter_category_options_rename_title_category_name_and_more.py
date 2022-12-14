# Generated by Django 4.1 on 2022-11-01 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0020_category"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Category", "verbose_name_plural": "Categories"},
        ),
        migrations.RenameField(
            model_name="category",
            old_name="title",
            new_name="name",
        ),
        migrations.RemoveField(
            model_name="category",
            name="book",
        ),
        migrations.AddField(
            model_name="book",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="books.category",
            ),
        ),
    ]
