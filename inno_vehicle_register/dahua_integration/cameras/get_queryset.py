
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




