

from dahua_integration.cameras.models import BufferTable
import os

def scheduled_job():


    # not_processed_objs = BufferTable.objects.filter(status='not processed').order_by('timestamp')[:4]
    # print('not_processed_objs: ', not_processed_objs)


    # # Change the status
    # for not_processed_obj in not_processed_objs:
    #     not_processed_obj.status = 'processed'
    #     not_processed_obj.save()

    f = open("/usr/src/app/dahua_integration/demofile2.txt", "a")
    f.write("Now the file has more content\n")
    f.close()

