
from django.db import models

class Camera(models.Model):
  name = models.CharField(max_length=255)
  direction = models.IntegerField( default=1)
  ip_address = models.CharField(max_length=100)
  port = models.CharField(max_length=50)
  status = models.CharField(max_length=100, default='offline')
  subscribe = models.BooleanField(default=False)
  username = models.CharField(max_length=255, default='admin')
  password = models.CharField(max_length=255, default='admin123')
  


# class VehicleInfo(models.Model):
#   plate_number = models.CharField(max_length=255)
#   prod_year = models.IntegerField(max_length=255, null=True)
#   vehicle_type = models.IntegerField(max_length=255, null=True)
#   serial_number = models.CharField(max_length=255)
#   latest_location = models.CharField(max_length=255)
#   vehicle_color = models.CharField(null=True, blank=True)
#   plate_image = models.ImageField(upload_to='small/', null=True)
#   vehicle_image = models.ImageField(upload_to='global/', null=True)

class Vehicle(models.Model):
  # This Vehicle model will be included with toll payment cameras and Dahua cameras connected via SDK.
  # vehicle_info_id = models.ForeignKey(VehicleInfo, on_delete=models.CASCADE, null)
  camera_id = models.CharField(max_length=255, null=True)
  camera_name= models.CharField(max_length=255, null=True)
  camera_direction = models.IntegerField( default=1)
  timestamp = models.DateTimeField()
  platenumber = models.CharField(max_length=255)
  platenumber_score = models.CharField(max_length=255, null=True)
  platenumber_fix = models.CharField(max_length=255, null=True)
  platenumber_fix_req = models.BooleanField(default=False)
  vehiclecolor = models.CharField(max_length=255)
  vehicletype = models.IntegerField(null=True, blank=True)
  plate_image = models.ImageField(upload_to='small/', null=True)
  vehicle_image = models.ImageField(upload_to='global/', null=True)
  avg_speed = models.CharField(max_length=255, null=True)
  is_trailer_check = models.BooleanField(default=False)
  is_trailer = models.BooleanField(default=False)


class BufferTable(models.Model):
  camera_id = models.CharField(max_length=255, null=True)
  vehicle_image = models.ImageField(upload_to='buffer/global/')
  plate_image = models.ImageField(upload_to='buffer/small/')
  vehiclecolor = models.CharField(max_length=255, default='Black')
  timestamp = models.DateTimeField()
  status = models.CharField(max_length=100, default='not processed')


class User(models.Model):
  username = models.CharField(max_length=20, null=False)
  password = models.CharField(max_length=50, null=False)
  timestamp = models.DateTimeField()
  status = models.BooleanField(default=True)
  

