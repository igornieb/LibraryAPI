# Generated by Django 4.2.1 on 2023-05-11 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_bookinstance_is_avilable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(to='core.author'),
        ),
    ]