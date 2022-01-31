import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortUrls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_url', models.TextField(verbose_name='URL')),
                ('short_url', models.TextField(verbose_name='Короткий URL')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='Создан')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.session', verbose_name='Сессия пользователя')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
