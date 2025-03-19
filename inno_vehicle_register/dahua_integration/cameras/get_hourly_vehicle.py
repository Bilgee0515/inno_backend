from django.utils import timezone
from datetime import timedelta, datetime
from .get_queryset import *


from .models import Vehicle

def get_hourly_vehicle(start_time, end_time):
    print("function:get_hourly_vehicle---> START")
    
    #start_time and end_time should be in datetime format
    print("start_time", start_time)
    print("end_time", end_time)

    # Timestamp__gte=start_time
    # Timestamp__lt=end_time

    # filter_condition = {'Start': start_time, 'End': end_time}
    querytype = "time_range"
    
    # queryset = get_queryset(querytype, Timestamp__gte=start_time, Timestamp__lt=end_time)
    queryset = get_queryset(querytype, filter_condition1={'timestamp__gte': start_time}, filter_condition2={'timestamp__lt': end_time})
    
    # # Filter vehicles based on the timestamp range
    # vehicles = Vehicle.objects.filter(Timestamp__gte=start_time, Timestamp__lt=end_time)


    for object in queryset:
        print(f"Vehicle ID: {object.id}")
        print(f"Camera ID: {object.camera_id}")
        print(f"Timestamp: {object.timestamp}")
        print(f"Platenumber: {object.platenumber}")
        print(f"Vehiclecolor: {object.vehiclecolor}")
        print(f"Vehicletype: {object.vehicletype}")

    print("function:get_hourly_vehicle---> END")
    

    return queryset


