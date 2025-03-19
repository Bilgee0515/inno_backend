# Generated by Django 4.2.7 on 2025-03-12 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BufferTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_id', models.CharField(max_length=255, null=True)),
                ('vehicle_image', models.ImageField(upload_to='buffer/global/')),
                ('plate_image', models.ImageField(upload_to='buffer/small/')),
                ('vehiclecolor', models.CharField(default='Black', max_length=255)),
                ('timestamp', models.DateTimeField()),
                ('status', models.CharField(default='not processed', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('direction', models.IntegerField(default=1)),
                ('ip_address', models.CharField(max_length=100)),
                ('port', models.CharField(max_length=50)),
                ('status', models.CharField(default='offline', max_length=100)),
                ('subscribe', models.BooleanField(default=False)),
                ('username', models.CharField(default='admin', max_length=255)),
                ('password', models.CharField(default='admin123', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField()),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_id', models.CharField(max_length=255, null=True)),
                ('camera_name', models.CharField(max_length=255, null=True)),
                ('camera_direction', models.IntegerField(default=1)),
                ('timestamp', models.DateTimeField()),
                ('platenumber', models.CharField(max_length=255)),
                ('platenumber_score', models.CharField(max_length=255, null=True)),
                ('platenumber_fix', models.CharField(max_length=255, null=True)),
                ('platenumber_fix_req', models.BooleanField(default=False)),
                ('vehiclecolor', models.CharField(max_length=255)),
                ('vehicletype', models.IntegerField(blank=True, null=True)),
                ('plate_image', models.ImageField(null=True, upload_to='small/')),
                ('vehicle_image', models.ImageField(null=True, upload_to='global/')),
                ('avg_speed', models.CharField(max_length=255, null=True)),
                ('is_trailer_check', models.BooleanField(default=False)),
                ('is_trailer', models.BooleanField(default=False)),
            ],
        ),
    ]
