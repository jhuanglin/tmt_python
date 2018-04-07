# Generated by Django 2.0.3 on 2018-04-07 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('_project', '0002_auto_20180407_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='done_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='list',
            name='end_time',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='list',
            name='start_time',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='list',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='_project.Status'),
        ),
        migrations.AlterField(
            model_name='list',
            name='summary',
            field=models.TextField(null=True),
        ),
    ]
