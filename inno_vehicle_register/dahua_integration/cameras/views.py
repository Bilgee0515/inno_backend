# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404, render, redirect
# from .models import Camera, Vehicle
# from NetSDK.NetSDK import NetClient
# from NetSDK.SDK_Struct import *
# from NetSDK.SDK_Enum import *
# from NetSDK.SDK_Callback import *
# from .sdk_function import *
# from .forms import CameraForm
# from .anpr_function import *
# from .get_hourly_vehicle import *
# from .get_count_vehicle import *
# from openpyxl import *
# from django.contrib import messages
# import sys
# from datetime import datetime
# from openpyxl.utils import get_column_letter

# callback_num = 0


# #Cameralist homepage view
# def cameras(request):
    
#     data = Camera.objects.all()  

#     return render(request, 'cameralist.html', {'data': data})

# # #viewlist homepage view test
# # def vehicle(request, filter_condition = None):
# #     if filter_condition is not None:
# #         data = Vehicle.objects.filter(filter_condition)  
# #     else:
# #         data = Vehicle.objects.all()

# #     return render(request, 'vehiclelist.html', {'data': data})


# def vehicle(request):

#     data = Vehicle.objects.all()

#     return render(request, 'vehiclelist.html', {'data': data})

# # camera connection 
# def connect_camera(request, pk):    
#     print("connect_camera function ---> START")

#     print("pk: ", pk)

#     #get camera object
#     camera = get_object_or_404(Camera, pk=pk)

#     ip = camera.ip_address
#     print("ip: ", ip)
#     port = camera.port
#     print("Port: ", port)
#     username = camera.username
#     print("username: ", username)
#     password = camera.password
#     print("password: ", password)

#     #SDK function camera login
#     loginID, device_info, error_msg, dwAlarmType = camera_login(ip, port, username, password)

#     print("loginID: ", loginID)
#     print("device_info: ", device_info)
#     print("error_msg: ", error_msg)


#     if len(error_msg) == 0:
#         print("Successful login")
#         item = get_object_or_404(Camera, pk=pk)
#         print("item_status: ", item.status)
#         item.status= 'online'
#         item.save()
#         message = "Camera connected successfully"
#         return HttpResponse(message)
#     else:
#         print("Unsuccessful login")
#         item = get_object_or_404(Camera, pk=pk)
#         print("item_status: ", item.status)
#         item.status = 'offline'
#         item.save()
#         error_message = "Error connecting to camera"
#         return HttpResponse(error_message, status=500)
        
# def subscribe_camera(request, pk):
#     print("subscribe_camera function ---> START")

#     camera = get_object_or_404(Camera, pk=pk)

#     ip = camera.ip_address
#     print("ip: ", ip)
#     port = camera.port
#     print("Port: ", port)
#     username = camera.username
#     print("username: ", username)
#     password = camera.password
#     print("password: ", password)

#     loginID, device_info, error_msg, dwAlarmType = camera_login(ip, port, username, password)
#     camera = get_object_or_404(Camera, pk=pk)
#     print("pk: ", pk)
#     dwUser = pk
#     print("camera: ", camera)
#     print('camera_status: ', camera.status)
#     if camera.status == "online":
#         attachID = camera_subscribe(loginID, device_info, error_msg, dwAlarmType, dwUser)
#         print("attachID: ", attachID)



#         if attachID > 0:
#             camera.subscribe = True
#             camera.save()
#             message = "Successful subscription!"
#             return HttpResponse(message)


#         else:
#             camera.subscribe = False
#             camera.save()
#             error_msg = "Unsuccessful subscription!"
#             return HttpResponse(error_msg, status=501)
        
#     else:
#         return connect_camera(request, pk)

# def add_camera(request):
#     if request.method == 'POST':
#         form = CameraForm(request.POST)
#         if form.is_valid():
#             new_camera = form.save(commit=False)
#             new_camera.save()
#             return redirect('cameras') 
#     else:
#         form = CameraForm()
#         print(sys.path)
#     return render(request, 'add_camera.html', {'form': form})

# def serialize_object(obj):
#     # Convert datetime objects to strings with timezone information stripped
#     return {
#         'timestamp': obj['timestamp'].astimezone().replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S') if 'timestamp' in obj else None,
#         'camera_id': obj.get('camera_id'),
#         'platenumber': obj.get('platenumber'),
#         'vehiclecolor': obj.get('vehiclecolor'),
#         'vehicletype': obj.get('vehicletype'),
#     }

# def get_report(request):
#     if request.method == 'GET':
#         start_time = request.GET.get('start_time')
#         end_time = request.GET.get('end_time')
#         queryset = get_hourly_vehicle(start_time, end_time)

#         # Create the Excel file
#         response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = 'attachment; filename=report.xlsx'

#         wb = Workbook()
#         ws = wb.active
#         ws.title = "Report"

#         headers = ["timestamp", "camera_id", "platenumber", "vehiclecolor", "vehicletype"]
#         ws.append(headers)

#         for vehicle in queryset:
#             serialized_vehicle = serialize_object({
#                 'timestamp': vehicle.timestamp,
#                 'camera_id': vehicle.camera_id,
#                 'platenumber': vehicle.platenumber,
#                 'vehiclecolor': vehicle.vehiclecolor,
#                 'vehicletype': vehicle.vehicletype,
#             })
#             ws.append([serialized_vehicle[key] for key in headers])

#         # Save the workbook to the response
#         wb.save(response)

#         # Render the template with the queryset
#         return response

#     return HttpResponse("Invalid request method")


# def get_daily_report(request):
#     try:
#         if request.method == 'GET':
#             # Get the selected date from the form submission
#             selected_date_str = request.GET.get('selected_date')

#             # Result is given within List with dict. timerange as keys and values are count
#             result_list = get_daily_count_list(selected_date_str)

#             # Load the Excel template
#             template_path = 'C:\\Users\\bilgee work\\Desktop\\dahua sdk django\\dahua_integration\\template.xlsx'
#             template_wb = load_workbook(template_path)
#             template_wb.properties.calculate_formula = True
#             template_ws = template_wb.active


#             print('result_dict: ', result_list)

#             # Update sheets
#             for time_range in range(1, 25):
#                 for timerange_dict in result_list:
#                     counts = timerange_dict.get(str(time_range), [])
#                     start_column = 'C'
#                     start_row = get_start_row(time_range)

#                     # Update cells with the values from the list
#                     for index, value in enumerate(counts):
#                         column_letter = chr(ord(start_column) + index)
#                         cell_coordinates = f"{column_letter}{start_row}"
#                         template_ws[cell_coordinates] = value
            
#             #update the date in excel
#             date_cell = 'M6'
#             template_ws[date_cell] = selected_date_str

#             #Calculate sum of the counts
           
#             start_row = 14
#             end_row = 37

#             # Loop through each column and add SUM formula in row 38
#             for col_idx in range(3, 14):
#                 col_letter = get_column_letter(col_idx)
#                 sum_formula = f'=SUM({col_letter}{start_row}:{col_letter}{end_row})'
#                 template_ws[f'{col_letter}38'] = sum_formula

#             # Add the sum of column C to M and store in column N for row 38
#             template_ws['N38'] = f'=SUM(C38:M38)'

#             template_wb.properties.calculate_formula = True

#             # Save the new workbook
#             response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             response['Content-Disposition'] = 'attachment; filename=daily_report.xlsx'
#             template_wb.save(response)

#             # Return the new workbook as a response
#             return response

#     except Exception as e:
#         # Handle exceptions and return an error response
#         return HttpResponse(f"Error: {str(e)}", status=500)



    











