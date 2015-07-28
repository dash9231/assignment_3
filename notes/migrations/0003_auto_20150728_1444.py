# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_auto_20150714_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='due',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
