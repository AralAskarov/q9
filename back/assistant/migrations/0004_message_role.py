# Generated by Django 5.1.2 on 2024-10-19 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0003_remove_message_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('assistant', 'Assistant')], default='user', max_length=10),
            preserve_default=False,
        ),
    ]
