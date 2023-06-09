# Generated by Django 4.2.1 on 2023-05-11 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_author_remove_book_author_book_authors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowedbook',
            name='book',
        ),
        migrations.RemoveField(
            model_name='borrowedbook',
            name='user',
        ),
        migrations.AddField(
            model_name='book',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='libraryuser',
            name='user_type',
            field=models.CharField(choices=[('S', 'Staff'), ('U', 'User')], default='U', max_length=1),
        ),
        migrations.DeleteModel(
            name='BookInstance',
        ),
        migrations.DeleteModel(
            name='BorrowedBook',
        ),
    ]
