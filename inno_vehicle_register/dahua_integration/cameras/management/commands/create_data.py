import os
import shutil
from django.core.management.base import BaseCommand, CommandError
from cameras.models import Vehicle, Camera
from django.utils import timezone
from django.core.files import File

from django.conf import settings


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        # for poll_id in options["poll_ids"]:
        plate_source_image_path = r"C:\users\sat\Downloads\Small_Img2.jpg"
        vehicle_source_image_path = r"C:\users\sat\Downloads\Global_Img3.jpg"

        plate_image_folder = os.path.join(settings.MEDIA_ROOT, 'small')
        vehicle_image_folder = os.path.join(settings.MEDIA_ROOT, 'global')

        plate_image_path = shutil.copy(plate_source_image_path, plate_image_folder)
        vehicle_image_path = shutil.copy(vehicle_source_image_path, vehicle_image_folder)

        try:
            Vehicle.objects.create(camera_id="1", timestamp=timezone.now(), platenumber="1111 abc", platenumber_score="80", platenumber_fix= "1111 abc", platenumber_fix_req=False, vehiclecolor="red", vehicletype=1, plate_image=plate_image_path, vehicle_image=vehicle_image_path, avg_speed="85")

            Vehicle.objects.create(camera_id="2", timestamp=timezone.now(), platenumber="2222 abc", platenumber_score="95", platenumber_fix= "2222 abc", platenumber_fix_req=False, vehiclecolor="black", vehicletype=2, plate_image=plate_image_path, vehicle_image=vehicle_image_path, avg_speed="95")

            Camera.objects.create(name="camera2", ip_address="192.168.0.2", port="5000", status="test", subscribe=True, username="admin", password="123")

        except Vehicle.DoesNotExist:
            raise CommandError('Poll does not exist')


        self.stdout.write(
            self.style.SUCCESS('Successfully created vehicle')
        )