# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-21 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cherkasov', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='avatar',
            field=models.ImageField(default='/uploads/avatars/user-noavatar.gif', upload_to='avatars'),
        ),
    ]