# Generated by Django 3.0.3 on 2020-04-13 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlantTip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipText', models.CharField(max_length=500)),
                ('tipTitle', models.CharField(max_length=30)),
            ],
        ),
    ]
