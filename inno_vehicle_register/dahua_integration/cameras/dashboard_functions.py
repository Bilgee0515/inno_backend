from datetime import datetime

from django.db import IntegrityError
from .time_difference import *
from .anpr_function import *
from .speed_calculation import *
from .get_vehicle_type import *
from .models import *

def capture_process():
    print('CAPTURE PROCESS FUNCTION ----START')
    #get not processed objects
    not_processed_objs = BufferTable.objects.filter(status='not processed').order_by('timestamp')[:4]
    print('not_processed_objs: ', not_processed_objs)

    #update status to processed
    for not_processed_obj in not_processed_objs:
        not_processed_obj.status = 'in process'
        not_processed_obj.save()

    
    #process each objects and create list of dict
    processed_obj_list = []
    for obj in not_processed_objs:
        print('obj.plateimage: ', obj.plate_image)
        platenumber, platealph, plate_number_score = anpr_function(str(obj.plate_image))
        lic_plate = platenumber + platealph
        avg_speed = speed_calculation()
        print("avg_speed: ", avg_speed)
        vehicle_type = get_vehicle_type(lic_plate)
        platenumber_fix_requi = False
        if plate_number_score < 80:
            platenumber_fix_requi = True
        vehicle_list = Vehicle.objects.filter(platenumber=lic_plate).filter(camera_id=obj.camera_id).order_by('-timestamp')
        print('vehicle_list: ', vehicle_list)
        if len(vehicle_list) == 0:
            vehicle = Vehicle.objects.create(
            camera_id=obj.camera_id, 
            timestamp=obj.timestamp, 
            platenumber=lic_plate, 
            platenumber_score=plate_number_score, 
            vehiclecolor=obj.vehiclecolor, 
            plate_image=obj.plate_image, 
            vehicle_image=obj.vehicle_image, 
            avg_speed = avg_speed, 
            vehicletype = vehicle_type, 
            platenumber_fix_req=platenumber_fix_requi 
            )
            print('new added Vehicle: ', vehicle)

        else:
            #get the latest object and check the timestamp
            vehicle = vehicle_list[0]
            #if the time_diff is less than time_diff it doesnt need to be added to vehicles
            print("obj.timestamp: ", obj.timestamp)
            print("prev_obj['timestamp']: ", vehicle.timestamp)
            time_diffs = time_difference(obj.timestamp, vehicle.timestamp)
            if time_diffs < 60:
                pass
            else:
                vehicle = Vehicle.objects.create(
                camera_id=obj.camera_id, 
                timestamp=obj.timestamp, 
                platenumber=lic_plate, 
                platenumber_score=plate_number_score, 
                vehiclecolor=obj.vehiclecolor, 
                plate_image=obj.plate_image, 
                vehicle_image=obj.vehicle_image, 
                avg_speed = avg_speed, 
                vehicletype = vehicle_type, 
                platenumber_fix_req=platenumber_fix_requi 
                )
                print('new added Vehicle: ', vehicle)

                        #create dict
        obj_dict = {
            "id": obj.id,
            "camera_id": obj.camera_id,
            "lic_plate": lic_plate,
            "timestamp": obj.timestamp
        }
        #save dict into list
        processed_obj_list.append(obj_dict)
             
        
        

        # for prev_obj in processed_obj_list:
        #     if obj.camera_id == prev_obj['camera_id'] and lic_plate == prev_obj['lic_plate']:
        #         print("obj.timestamp: ", obj.timestamp)
        #         print("prev_obj['timestamp']: ", prev_obj['timestamp'])
        #         time_diff = time_difference(obj.timestamp, prev_obj['timestamp'])
        #         if time_diff < 60:
        #             pass

        #         else:
        #             # get object from vehicle table with matching lic plate and camera id ordered by newest
        #             vehicle_list = Vehicle.objects.filter(platenumber=lic_plate).filter(camera_id=obj.camera_id).order_by('timestamp')
        #             print('vehicle_list: ', vehicle_list)

        #             #if the list comes empty create the obj
        #             if len(vehicle_list) == 0:
        #                 vehicle = Vehicle.objects.create(
        #                 camera_id=obj.camera_id, 
        #                 timestamp=obj.timestamp, 
        #                 platenumber=lic_plate, 
        #                 platenumber_score=plate_number_score, 
        #                 vehiclecolor=obj.vehicle_color, 
        #                 plate_image=obj.plate_image, 
        #                 vehicle_image=obj.vehicle_image, 
        #                 avg_speed = avg_speed, 
        #                 vehicle_type = vehicle_type, 
        #                 platenumber_fix_req=platenumber_fix_requi 
        #                 )
        #                 print('new added Vehicle: ', vehicle)
        #             else:
        #                 #get the latest object and check the timestamp
        #                 vehicle = vehicle_list[0]
        #                 #if the time_diff is less than time_diff it doesnt need to be added to vehicles
        #                 print("obj.timestamp: ", obj.timestamp)
        #                 print("prev_obj['timestamp']: ", vehicle.timestamp)
        #                 time_diffs = time_difference(obj.timestamp, vehicle.timestamp)
        #                 if time_diffs < 60:
        #                     pass
        #                 else:
        #                     vehicle = Vehicle.objects.create(
        #                     camera_id=obj.camera_id, 
        #                     timestamp=obj.timestamp, 
        #                     platenumber=lic_plate, 
        #                     platenumber_score=plate_number_score, 
        #                     vehiclecolor=obj.vehicle_color, 
        #                     plate_image=obj.plate_image, 
        #                     vehicle_image=obj.vehicle_image, 
        #                     avg_speed = avg_speed, 
        #                     vehicle_type = vehicle_type, 
        #                     platenumber_fix_req=platenumber_fix_requi 
        #                     )
        #                     print('new added Vehicle: ', vehicle)

                            

        # #create dict
        # obj_dict = {
        #     "id": obj.id,
        #     "camera_id": obj.camera_id,
        #     "lic_plate": lic_plate,
        #     "timestamp": obj.timestamp
        # }
        # #save dict into list
        # processed_obj_list.append(obj_dict)

            




def camera_status():

    online_cam_list= []
    cameras = Camera.objects.all()
    for camera in cameras:
        if camera.status == "online":
            online_cam_dict = {
                "camera_id" : camera.id,
                'camera_name': camera.name,
                'camera_status': camera.status
            }
            online_cam_list.append(online_cam_dict)

    cam_num_online = len(online_cam_list)
    cam_num_total = len(cameras)

    return cam_num_online, cam_num_total

def speeding_count():
    vehicles = Vehicle.objects.filter(avg_speed__gt=80)
    vehicle_num = len(vehicles)

    return vehicle_num

def average_rec_score():
    vehicles = Vehicle.objects.all()
    vehicle_num = len(vehicles)
    vehicle_score_list = []
    for vehicle in vehicles:
        score = int(vehicle.platenumber_score)
        vehicle_score_list.append(score)

    total_score = 0
    for vehicle_score in vehicle_score_list:
        total_score = total_score + vehicle_score

    average_rec = total_score / vehicle_num

    return average_rec

def vehicle_count():
    vehicles = Vehicle.objects.all()
    vehicle_num = len(vehicles)

    return vehicle_num

    

        
