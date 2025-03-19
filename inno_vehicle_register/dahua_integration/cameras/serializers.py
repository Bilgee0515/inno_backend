from rest_framework import serializers
from .models import Camera, Vehicle, BufferTable

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

class BufferTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = BufferTable
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    camera_name = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = ['id', 'timestamp', 'platenumber', 'platenumber_score', 'platenumber_fix', 'platenumber_fix_req', 'vehiclecolor', 'vehicletype', 'plate_image', 'vehicle_image', 'avg_speed', 'camera_name']

    def get_camera_name(self, obj):
        # Retrieve the camera name based on the camera_id of the vehicle
        if obj.camera_id:
            try:
                camera = Camera.objects.get(id=obj.camera_id)
                return camera.name
            except Camera.DoesNotExist:
                return None
        else:
            return None