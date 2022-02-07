from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shorturls',
            name='short_url',
            field=models.CharField(max_length=100, unique=True, verbose_name='Короткий URL'),
        ),
    ]
