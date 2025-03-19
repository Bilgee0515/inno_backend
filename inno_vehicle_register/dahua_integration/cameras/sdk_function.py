from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Camera, Vehicle, BufferTable
from NetSDK.NetSDK import NetClient
from NetSDK.SDK_Struct import *
from NetSDK.SDK_Enum import *
from NetSDK.SDK_Callback import *
# from .anpr_function import *
from .get_vehicle_type import *
from .speed_calculation import *
from django.conf import settings
from django.db import IntegrityError


sdk = NetClient()
sdk.InitEx()

callback_num = 0


class TrafficCallBackAlarmInfo:
    def __init__(self):
        time_str = ""
        plate_number_str = ""
        plate_color_str = ""
        object_subType_str = ""
        vehicle_color_str = ""




    ###
    # Get alarm info
    #  
    ###
    def get_alarm_info(self, alarm_info):
        time_str = '{}-{}-{} {}:{}:{}'.format(alarm_info.UTC.dwYear, alarm_info.UTC.dwMonth, alarm_info.UTC.dwDay,
                                                   alarm_info.UTC.dwHour, alarm_info.UTC.dwMinute, alarm_info.UTC.dwSecond)
        # plate_number_str = str(alarm_info.stTrafficCar.szPlateNumber.decode('gb2312'))
        plate_number_str = str(alarm_info.stTrafficCar.szPlateNumber.decode('cp1251'))
        plate_color_str = str(alarm_info.stTrafficCar.szPlateColor, 'utf-8')
        object_subType_str = str(alarm_info.stuVehicle.szObjectSubType, 'utf-8')
        vehicle_color_str = str(alarm_info.stTrafficCar.szVehicleColor, 'utf-8')

        # print("plate_number_str: ", plate_number_str)
        # print("time_str: ", time_str)
        # print("vehicle_color_str: ", vehicle_color_str)

        # print("plate recognized from cam is: ", plate_number_str)

        # Vehicle.objects.create(CameraID=, Timestamp=time_str, Platenumber=plate_number_str, Vehiclecolor=vehicle_color_str) 


@CB_FUNCTYPE(None, C_LLONG, C_DWORD, c_void_p, POINTER(c_ubyte), C_DWORD, C_LDWORD, c_int, c_void_p)
def AnalyzerDataCallBack(lAnalyzerHandle, dwAlarmType, pAlarmInfo, pBuffer, dwBufSize, dwUser, nSequence, reserved):
    print('Enter AnalyzerDataCallBack')

    # 当报警类型是交通卡口事件时在界面上进行显示相关信息
    if(dwAlarmType == EM_EVENT_IVS_TYPE.TRAFFICJUNCTION):
        global callback_num
        local_path = os.path.abspath('./media')
        print("local_path: ", local_path)
        is_global = False
        is_small = False
        show_info = TrafficCallBackAlarmInfo()
        callback_num += 1
        alarm_info = cast(pAlarmInfo, POINTER(DEV_EVENT_TRAFFICJUNCTION_INFO)).contents
        print('alarm_info: ', alarm_info)
        show_info.get_alarm_info(alarm_info)
        if alarm_info.stuObject.bPicEnble:
            is_global = True
            GlobalScene_buf = cast(pBuffer,POINTER(c_ubyte * alarm_info.stuObject.stPicInfo.dwOffSet)).contents
            if not os.path.isdir(os.path.join(local_path, 'Global')):
                os.mkdir(os.path.join(local_path, 'Global'))
            with open('./media/Global/Global_Img' + str(callback_num) + '.jpg', 'wb+') as global_pic:
                global_pic.write(bytes(GlobalScene_buf))
            if (alarm_info.stuObject.stPicInfo.dwFileLenth > 0):
                is_small = True
                small_buf = pBuffer[alarm_info.stuObject.stPicInfo.dwOffSet:alarm_info.stuObject.stPicInfo.dwOffSet +
                                                                        alarm_info.stuObject.stPicInfo.dwFileLenth]
                if not os.path.isdir(os.path.join(local_path, 'Small')):
                    os.mkdir(os.path.join(local_path, 'Small'))
                with open('./media/Small/Small_Img' + str(callback_num) + '.jpg', 'wb+') as small_pic:
                    small_pic.write(bytes(small_buf))
        elif (dwBufSize > 0):
            is_global = True
            GlobalScene_buf = cast(pBuffer, POINTER(c_ubyte * dwBufSize)).contents
            if not os.path.isdir(os.path.join(local_path, 'Global')):
                os.mkdir(os.path.join(local_path, 'Global'))
            with open('./Global/Global_Img' + str(callback_num) + '.jpg', 'wb+') as global_pic:
                global_pic.write(bytes(GlobalScene_buf))

        # yum butsaadaggui baisniig zurgiin path butsaadag bolgon uurchluw
        url_path = 'Small/Small_Img' + str(callback_num) + '.jpg'
        vehicle_url_path = 'Global/Global_Img' + str(callback_num) + '.jpg'

        print('small path: ',url_path)
        print('global path: ',vehicle_url_path)



        
        

        # platenumber, platealph, plate_number_score = anpr_function(url_path)
        # print('platenumber: ', platenumber)
        # print('platealph: ', platealph)
        # plate_spaced = platenumber + platealph


        # print("plate recognized from sw is: ", plate_spaced)
        # print("algorithm recognized score: ", plate_number_score)
        # platenumber_fix_requi = False
        # if plate_number_score < 80:
        #     platenumber_fix_requi = True

        print("alarm_info", alarm_info)

        time_str = '{}-{}-{} {}:{}:{}'.format(alarm_info.UTC.dwYear, alarm_info.UTC.dwMonth, alarm_info.UTC.dwDay,
                                            alarm_info.UTC.dwHour, alarm_info.UTC.dwMinute, alarm_info.UTC.dwSecond)
        vehicle_color_str = str(alarm_info.stTrafficCar.szVehicleColor, 'utf-8')

        print("time_str: ", time_str)

        timestamp_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

        print("timestamp_obj: ", timestamp_obj)

        #creating buffertable object 
        try:

            buffer_obj = BufferTable.objects.create(camera_id=dwUser, timestamp=timestamp_obj, plate_image=url_path, vehicle_image=vehicle_url_path, vehiclecolor=vehicle_color_str)
            print("Object created successfully:", buffer_obj)

        except IntegrityError as e:
            print("Object creation failed:", e)


        return
    

def cameras(request):
    
    data = Camera.objects.all()  

    return render(request, 'cameralist.html', {'data': data})

# camera login function
def camera_login(ip, port, username, password):

    print("Login into camera Function ---->START")

    stuInParam = NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY()
    stuInParam.dwSize = sizeof(NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY)
    stuInParam.szIP = ip.encode()
    stuInParam.nPort = int(port)
    stuInParam.szUserName = username.encode()
    stuInParam.szPassword = password.encode()
    stuInParam.emSpecCap = EM_LOGIN_SPAC_CAP_TYPE.TCP
    stuInParam.pCapParam = None



    stuOutParam = NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY()
    stuOutParam.dwSize = sizeof(NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY)

    print('stuInParam and stuOutParam are SET')
    dwAlarmType = EM_EVENT_IVS_TYPE.TRAFFICJUNCTION

    #Login to camera
    loginID, device_info, error_msg = sdk.LoginWithHighLevelSecurity(stuInParam, stuOutParam)

    print("Login into camera Function ---->END")


    return loginID, device_info, error_msg, dwAlarmType


def camera_subscribe(loginID, device_info, error_msg, dwAlarmType, dwUser):
    print("camera_subscribe Function ---->START")


    channel = 0
    bNeedPicFile = 0
    #dwUser = 0

    #subscribe to intelligent data
    # attachID, url_path = sdk.RealLoadPictureEx(loginID, channel, dwAlarmType, bNeedPicFile, AnalyzerDataCallBack, dwUser, None)
    attachID = sdk.RealLoadPictureEx(loginID, channel, dwAlarmType, bNeedPicFile, AnalyzerDataCallBack, dwUser, None)

    #url path butsaagad terugere dugaar tanina
    # print('url_path: ', url_path)
    

    # static_url_path = './Global/Global_Img5.jpg'
    # platenumber, platealph = anpr_function(static_url_path)

    # print('platenumber: ', platenumber)
    # print('platealph: ', platealph)

    print("attachID: ", attachID)
    if not attachID:
        print("Error occured while subscribing")
    else:
        print("Subscribe Success")
    return  attachID


def camera_unsubscribe(attachID):
    if (attachID == 0):
        return
    sdk.StopLoadPic(attachID)
    attachID = 0
