
from datetime import datetime, timedelta
from .models import Vehicle
from django.db.models import Q

def get_queryset(querytype, filter_condition1=None, filter_condition2=None):
    print("function:get_queryset---> START")

    if filter_condition1 is None and querytype == "all":
        queryset = Vehicle.objects.all()

    if querytype == "filter":

        queryset = Vehicle.objects.filter(**filter_condition1)


    if querytype == "time_range":
        queryset = Vehicle.objects.filter(Q(**filter_condition1) & Q(**filter_condition2))

    else:
        raise ValueError("Invalid query_type or missing filter_param")


    print("function:get_queryset---> END")

    return queryset

def get_count_vehicle(start_time, end_time, vehicle_type, selected_camera):
    # TODO: get queryset based on arguments
    # TODO: count the objects that came within queryset
    # TODO: define count and return it
    count = "5"
    return count

def get_daily_count_list(selected_date, selected_camera):
    # 9 types of vehicles
    result_list = []

    for time_range in range(1, 25):
        start_time, end_time = time_range_to_start_end_time(time_range, selected_date)

        type_counts = []
        for vehicle_type in range(1, 12):
            count = get_count_vehicle(start_time, end_time, vehicle_type, selected_camera)
            type_counts.append(count)

        result_dict = {str(time_range): type_counts}
        result_list.append(result_dict)

    return result_list

def time_range_to_start_end_time(time_range, selected_date):
    # Validate that time_range is within the range of 1 to 24
    if not (1 <= time_range <= 24):
        raise ValueError("Invalid time_range. It should be an integer between 1 and 24.")

    # Convert selected_date to a datetime object
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()

    # Calculate start_time and end_time based on the time_range and selected_date
    start_time_str = f"{time_range - 1:02}:00:00"
    end_time_str = f"{time_range:02}:00:00"

    # Handle special case for 24:00:00
    if time_range == 24:
        end_time = datetime.combine(selected_date + timedelta(days=1), datetime.min.time())
        start_time = datetime.combine(selected_date, datetime.min.time())
    else:
        # Combine date with time to create datetime objects
        start_time = datetime.combine(selected_date, datetime.strptime(start_time_str, '%H:%M:%S').time())
        end_time = datetime.combine(selected_date, datetime.strptime(end_time_str, '%H:%M:%S').time())

    return start_time, end_time




def get_count_each_type_by_time(start_time, end_time):
    #9 types of vehicles 
    count_list_by_time = []

    for vehicle_type in range(1, 12):
        
        count = get_count_vehicle(start_time, end_time, vehicle_type)

        count_list_by_time.append(count)


    return count_list_by_time

def get_start_row(time_range):
    if time_range == 1:
        start_row = 26
    if time_range == 2:
        start_row = 27
    if time_range == 3:
        start_row = 28
    if time_range == 4:
        start_row = 29
    if time_range == 5:
        start_row = 30
    if time_range == 6:
        start_row = 31
    if time_range == 7:
        start_row = 32
    if time_range == 8:
        start_row = 33
    if time_range == 9:
        start_row = 34
    if time_range == 10:
        start_row = 35
    if time_range == 11:
        start_row = 36
    if time_range == 12:
        start_row = 37
    if time_range == 13:
        start_row = 14
    if time_range == 14:
        start_row = 15
    if time_range == 15:
        start_row = 16
    if time_range == 16:
        start_row = 17
    if time_range == 17:
        start_row = 18
    if time_range == 18:
        start_row = 19
    if time_range == 19:
        start_row = 20
    if time_range == 20:
        start_row = 21
    if time_range == 21:
        start_row = 22
    if time_range == 22:
        start_row = 23
    if time_range == 23:
        start_row = 24
    if time_range == 24:
        start_row = 25

    return start_row

            


    





