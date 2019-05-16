# Generated by Django 2.0 on 2019-05-09 07:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20190507_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply_to_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='replies', to=settings.AUTH_USER_MODEL),
        ),
    ]
