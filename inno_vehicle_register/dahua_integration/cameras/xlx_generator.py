from django.utils import timezone
from datetime import timedelta, datetime


from .models import Vehicle

def get_queryset():
    print("get_queryset Function --->START")




    # Filter vehicles based on the timestamp range
    vehicles = Vehicle.objects.all()

    print("Vehicles in last hour", vehicles)
    # print("Vehicles in last hour", vehicles.id)
    # print("Vehicles in last hour", vehicles.Timestamp)
    # print("Vehicles in last hour", vehicles.Platenumber)
    for vehicle in vehicles:
        print(f"Vehicle ID: {vehicle.id}")
        print(f"Camera ID: {vehicle.CameraID}")
        print(f"Timestamp: {vehicle.Timestamp}")
        print(f"Platenumber: {vehicle.Platenumber}")
        print(f"Vehiclecolor: {vehicle.Vehiclecolor}")
        print(f"Vehicletype: {vehicle.Vehicletype}")

    return vehicles

def xlx_generator(queryset):
    print("xlx_generator function-->START")
    workbook = 1
    return workbook



