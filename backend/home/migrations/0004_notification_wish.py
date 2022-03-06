# Generated by Django 2.2.27 on 2022-03-06 01:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0003_delete_wish'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='Location')),
                ('created_at', models.DateField(default=django.utils.timezone.now, verbose_name='Notification Created Date Time')),
                ('is_read', models.BooleanField(default=False)),
                ('tee_time', models.DateField(default=django.utils.timezone.now, verbose_name='Time and Date')),
                ('no_of_selected_golfers', models.CharField(blank=True, max_length=255, null=True, verbose_name='Number of selected players')),
                ('no_of_slots_available', models.CharField(blank=True, max_length=255, null=True, verbose_name='Number of slots available')),
                ('no_of_max_players', models.CharField(blank=True, max_length=255, null=True, verbose_name='Number of maximum players for opened slot')),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='Location')),
                ('golfers', models.CharField(blank=True, max_length=255, null=True, verbose_name='Number of Golfers')),
                ('from_date', models.DateField(default=django.utils.timezone.now, verbose_name='From Date')),
                ('to_date', models.DateField(default=False, verbose_name='To Date')),
                ('is_before_selected', models.BooleanField(default=False)),
                ('created_at', models.DateField(default=django.utils.timezone.now, verbose_name='Created at')),
            ],
        ),
    ]