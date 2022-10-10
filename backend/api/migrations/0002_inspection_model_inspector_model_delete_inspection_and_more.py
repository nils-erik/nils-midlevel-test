# Generated by Django 4.0.8 on 2022-10-09 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='inspection_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.TextField(max_length=120)),
                ('city', models.TextField(max_length=120)),
                ('scheduledDate', models.TextField(max_length=120)),
                ('inspectorId', models.IntegerField()),
                ('items', models.JSONField()),
                ('company', models.CharField(default='', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='inspector_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.TextField(max_length=120)),
                ('name', models.TextField(max_length=120)),
                ('availableIntegrations', models.JSONField()),
                ('inspectorId', models.IntegerField()),
                ('company', models.CharField(default='', max_length=120)),
            ],
        ),
        migrations.DeleteModel(
            name='inspection',
        ),
        migrations.DeleteModel(
            name='inspector',
        ),
    ]