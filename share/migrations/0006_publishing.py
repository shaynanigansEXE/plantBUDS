# Generated by Django 3.0.3 on 2020-04-14 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0005_plantbuddy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publishing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=100)),
                ('subject', models.CharField(max_length=50)),
                ('body', models.TextField(max_length=10000)),
                ('make_public', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('plantbuddy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.PlantBuddy')),
            ],
        ),
    ]
