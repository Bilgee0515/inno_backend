# Refactored capture_process.py

from datetime import datetime
from django.db import IntegrityError
from .time_difference import *
from .anpr_function import *
from .speed_calculation import *
from .get_vehicle_type import *
from .models import *
import random
import string

def read_work_book():
    #this function should take excel workbook
    #and read the counts with date by the hours
    # return numbers of vehicle by the time with location
    return "test"

def take_dict_to_save():
    # takes a number report from the excel
    # and saves to the table by the locations
    # then return success or fail

    return "success"




#random function to generate platenumber
def random_plate_num():
    numbers = ''.join(random.choices(string.digits, k=4))  
    letters = ''.join(random.choices(string.ascii_uppercase, k=3)) 
    return numbers + letters


def capture_process():
    print('CAPTURE PROCESS FUNCTION ----START')

    not_processed_objs = BufferTable.objects.filter(status='not processed').order_by('-timestamp')[:4]

    # Process each object and create a list of processed objects
    processed_obj_list = []
    for obj in not_processed_objs:
        print('obj.plateimage: ', obj.plate_image)
        platenumber = random_plate_num()
        # platenumber = anpr_function(str(obj.plate_image))
        print('platenumber: ', platenumber)

        avg_speed = speed_calculation()
        print("avg_speed: ", avg_speed)
        vehicle_type = get_vehicle_type(platenumber)
        platenumber_fix_requi = False

        vehicle_list = Vehicle.objects.filter(platenumber=platenumber).filter(camera_id=obj.camera_id).order_by('-timestamp')
        print('vehicle_list: ', vehicle_list)
        if len(vehicle_list) == 0:
            vehicle = Vehicle.objects.create(
                camera_id=obj.camera_id, 
                timestamp=obj.timestamp, 
                platenumber=platenumber, 
                vehiclecolor=obj.vehiclecolor, 
                plate_image=obj.plate_image, 
                vehicle_image=obj.vehicle_image, 
                avg_speed=avg_speed, 
                vehicletype=vehicle_type, 
                platenumber_fix_req=platenumber_fix_requi 
            )
            print('new added Vehicle: ', vehicle)
        else:
            vehicle = vehicle_list[0]
            time_diffs = time_difference(obj.timestamp, vehicle.timestamp)
            if time_diffs < 60:
                pass
            else:
                vehicle = Vehicle.objects.create(
                    camera_id=obj.camera_id, 
                    timestamp=obj.timestamp, 
                    platenumber=platenumber, 
                    vehiclecolor=obj.vehiclecolor, 
                    plate_image=obj.plate_image, 
                    vehicle_image=obj.vehicle_image, 
                    avg_speed=avg_speed, 
                    vehicletype=vehicle_type, 
                    platenumber_fix_req=platenumber_fix_requi 
                )
                print('new added Vehicle: ', vehicle)

        obj_dict = {
            "id": obj.id,
            "camera_id": obj.camera_id,
            "lic_plate": platenumber,
            "timestamp": obj.timestamp
        }
        processed_obj_list.append(obj_dict)

    return processed_obj_list
