# Generated by Django 5.0.6 on 2024-08-03 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_comment_is_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='is_negative',
        ),
    ]