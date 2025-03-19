from django.urls import path
#TODO change after updating the views.py to apiview then change the import source line
from .views_drf import *

urlpatterns = [
    path('cameras/', CameraListView.as_view(), name = 'camera-list'),
    path('vehicles/', VehicleListView.as_view(), name = 'vehicle-list'),
    path('vehicles/check/', VehicleTrailerListView.as_view(), name = 'vehicle-trailer-list'),
    path('alerted-vehicles/', AlertedVehicleView.as_view(), name='alerted-vehicles-list'),
    path('update-vehicle/<int:pk>/', UpdateAlertedVehicleView.as_view(), name='update-vehicle'),
    path('connect_camera/<int:pk>/', ConnectCameraView.as_view(), name='connect-camera'),
    path('add_camera/', AddCameraView.as_view(), name='add-camera'),
    path('delete_camera/<int:pk>/', DeleteCameraView.as_view(), name='delete-camera'),
    path('get_report/', GetReportView.as_view(), name='get-report'),
    path('get_daily_report/', GetDailyReportView.as_view(), name='get-daily-report'),
    path('subscribe_camera/<int:pk>/', SubscribeCameraView.as_view(), name='subscribe-camera'),
    path('capture_process/', CaptureProcessView.as_view(), name='capture-process'),
    path('buffer_table/', BufferTableListView.as_view(), name='buffer-table-list'),
    path('add_buffer/', AddBufferTableView.as_view(), name='add-buffer'),
    path('daily_report/', GetDailyReportAllCamView.as_view(), name='get-daily-all-cam'),
    path('add_vehicle/', PostVehicleInfoView.as_view(), name='add-vehicle'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]