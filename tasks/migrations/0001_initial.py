# Generated by Django 4.2.18 on 2025-02-13 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_lists_created', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('priority', models.CharField(blank=True, choices=[('doFirst', 'Do First'), ('schedule', 'Schedule'), ('delegate', 'Delegate'), ('eliminate', 'Eliminate')], max_length=50, null=True)),
                ('position_x', models.FloatField(blank=True, null=True)),
                ('position_y', models.FloatField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('in_matrix', models.BooleanField(default=True)),
                ('item_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.itemlist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
