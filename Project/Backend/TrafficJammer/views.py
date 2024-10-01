from django.http import HttpResponse
from django.shortcuts import render
import pika
import json
import math
from datetime import datetime,timezone,timedelta
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import responses
from rest_framework import status
import traceback
from TrafficJammer.models import Street, \
    Section, \
    Transit, \
    Accident, \
    Car, \
    Blocked, \
    SectionSerializer, \
    StreetSerializer, \
    StreetInputSerializer, \
    StreetStatisticsSerializer, \
    CarSerializer, \
    AccidentSerializer, \
    AllStreetSerializer, \
    LicensesSerializer



@csrf_exempt
def info_street(request,city):
    try:
        if request.method=="GET":
            sections=Section.objects.filter(street__city=city)
            return HttpResponse(json.dumps(SectionSerializer(sections,many=True).data),status=status.HTTP_200_OK)
    except Section.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def street(request):
    try:
        if request.method=="POST":
            '''
            Creating a new street
            '''
            print("Creating a new street")
            data=json.loads(request.body)
            name=data.get("name")
            start = data.get("beginning_coords")
            end = data.get("ending_coords")
            city=data.get("city")
            if len(Street.objects.filter(city=city,begin_coord_x=start[0],begin_coord_y=start[1],ending_coord_x=end[0],ending_coord_y=end[1],name=name))>0:
                return HttpResponse("That street already exists",status=status.HTTP_409_CONFLICT)

            if start[0] < end[0]:
                x_length = end[0] - start[0]
                increase_x = 1
            else:
                x_length = start[0] - end[0]
                increase_x = -1

            if start[1] < end[1]:
                y_length = end[1] - start[1]
                increase_y = 1
            else:
                y_length = start[1] - end[1]
                increase_y = -1

            path_length = math.hypot(x_length, y_length)


            street_obj=Street(name=name,
                            begin_coord_x=start[0],
                            begin_coord_y=start[1],
                            ending_coord_x=end[0],
                            ending_coord_y=end[1],
                            length=path_length,
                            city=city)
            street_obj.save()
            '''
            Turning the street into different s ections
            Each section is aprox 500m of a street, if the street is made of sections that aren't divisible by 500
            the last section will be the rest 1200=500+500+200
            '''
            num_subsections = int(path_length//500) + 1
            end_section = tuple(start)

            for i in range(1, num_subsections):

                start_section = end_section
                end_section = (
                        start[0] + i*x_length/num_subsections*increase_x,
                        start[1] + i*y_length/num_subsections*increase_y
                    )

                create_section(street_obj,start_section[0], start_section[1],end_section[0], end_section[1], True)
                create_section(street_obj,start_section[0], start_section[1],end_section[0], end_section[1], False)

            create_section(street_obj, end_section[0], end_section[1], end[0], end[1], True)
            create_section(street_obj, end_section[0], end_section[1], end[0], end[1], False)

            return HttpResponse(json.dumps(StreetInputSerializer(street_obj).data),status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def car_to_street(request):
    try:
        if request.method=="POST":
            data=json.loads(request.body)
            crud_ops=data.get("data")
            for op in crud_ops:
                if op.get("type") == "insert":
                    section=Section.objects.get(id=op.get("id"))
                    section.number_cars+=1
                    car=Car(license_plate=op.get("plate"),section=section)
                    car.save()
                    add_to_transit(section)
                    section.save()
                elif op.get("type") == "delete":
                    section=Section.objects.get(id=op.get("id"))
                    section.number_cars-=1
                    car=Car.objects.get(license_plate=op.get("plate"))
                    car.delete()
                    section.save()
                else:
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(status=status.HTTP_200_OK)
    except Car.DoesNotExist:
        return HttpResponse("Car not found",status=status.HTTP_404_NOT_FOUND)
    except Section.DoesNotExist:
        return HttpResponse("Section not found",status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def add_to_accident(request):
    try:
        if request.method=="POST":
            data=json.loads(request.body)
            section=Section.objects.get(id=data.get("id"))
            accident= Accident(section=section,coord_x=data.get("x_coord"),coord_y=data.get("y_coord"),date=datetime.now(timezone.utc))
            accident.save()
            return HttpResponse(json.dumps(AccidentSerializer(accident).data),status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except Section.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

def add_to_transit(section,transit=80):
    time_of_transit = datetime.now(timezone.utc)
    last_time_of_transit = sorted(Transit.objects.filter(section=section),key=lambda transit:transit.date,reverse=True)
    if section.number_cars>transit:
        if last_time_of_transit==[]:
            street_transit = Transit(date=time_of_transit, section=section)
            street_transit.save()
        if last_time_of_transit[0].date+timedelta(minutes=30)<time_of_transit:
            street_transit = Transit(date=time_of_transit,section=section)
            street_transit.save()

def create_section(street,coord_x,coord_y,end_x,end_y,direction):
    section = Section(street=street,
                      beginning_coords_x=coord_x,
                      beginning_coords_y=coord_y,
                      ending_coords_x=end_x,
                      ending_coords_y=end_y,
                      actual_direction=direction)
    section.save()


def get_car(request,license_plate):
    try:
        if request.method=='GET':
            car=Car.objects.get(license_plate=license_plate)
            return HttpResponse(json.dumps(CarSerializer(car).data),status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except Car.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

def all_cars(request,section):
    try:
        if request.method=="GET":
            section=Section.objects.get(id=section)
            car=Car.objects.filter(section=section)
            return HttpResponse(json.dumps(CarSerializer(car,many=True).data),status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except Section.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

def statistics(request,street,begin,end,week_day=None):
    day_to_int={"Monday":2,"Tuesday":3,"Wednesday":4,"Thursday":5,"Friday":6,"Saturday":7,"Sunday":1}
    try:
        if request.method=="GET":
            begin_time=begin.split("-")
            begin_time=datetime(int(begin_time[0]), int(begin_time[1]), int(begin_time[2]), 0, 0, 0, 0, timezone.utc)
            end_time=end.split("-")
            end_time=datetime(int(end_time[0]),int(end_time[1]),int(end_time[2]),0,0,0,0,timezone.utc)
            street=Street.objects.get(id=street)
            section_list=Section.objects.filter(street=street)
            # Generation of empty query sets
            transit=Transit.objects.none()
            blocked=Blocked.objects.none()
            accident=Accident.objects.none()
            # iteration of each section of that street
            for section in section_list:
                temp_blocked=Blocked.objects.filter(section=section,begin__range=(begin_time,end_time),end__range=(begin_time,end_time))
                blocked = blocked | temp_blocked
                if week_day:
                    temp_transit = Transit.objects.filter(section=section,date__range=(begin_time, end_time),date__week_day=day_to_int.get(week_day))
                    temp_accident = Accident.objects.filter(section=section,date__range=(begin_time, end_time),date__week_day=day_to_int.get(week_day))
                    # Join of Query Sets
                    transit = transit | temp_transit
                    accident = accident | temp_accident
                else:
                    temp_transit=Transit.objects.filter(section=section,date__range=(begin_time,end_time))
                    temp_accident=Accident.objects.filter(section=section,date__range=(begin_time,end_time))
                    # Join of Query Sets
                    transit = transit | temp_transit
                    accident = temp_accident | temp_accident

            return HttpResponse(json.dumps(StreetStatisticsSerializer(street,
                                context={"transit":transit,"blocked":blocked,"accident":accident}).data),status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except Section.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def visibility(request):
    if request.method=="PUT":
        try:
            data=json.loads(request.body)
            section=Section.objects.get(id=data.get("id"))
            section.visibility=data.get("visibility")
            section.save()
            return HttpResponse(json.dumps(SectionSerializer(section).data),status=status.HTTP_200_OK)
        except Section.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def police(request):
    try:
        if request.method == "PUT":
            data= json.loads(request.body)
            section=Section.objects.get(id=data.get("id"))
            section.police=True
            section.save()
            return HttpResponse(json.dumps(SectionSerializer(section).data),status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            data=json.loads(request.body)
            section = Section.objects.get(id=data.get("id"))
            section.police = False
            section.save()
            return HttpResponse(json.dumps(SectionSerializer(section).data),status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except Section.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def roadblock(request):
    try:
        if request.method=="POST":
            data = json.loads(request.body)
            section = Section.objects.get(id=data.get("id"))
            section.roadblock=True
            section.save()
            if len(Blocked.objects.filter(section=section,end__isnull=True)):
                return HttpResponse("A road can only be blocked once",status=status.HTTP_304_NOT_MODIFIED)
            road_block=Blocked(section=section,begin=datetime.now(timezone.utc))
            road_block.save()
            return HttpResponse("Road Blocked",status=status.HTTP_200_OK)
        elif request.method=="DELETE":
            data = json.loads(request.body)
            road_block=Blocked.objects.get(section=data.get("id"),end__isnull=True)
            road_block.end=datetime.now(timezone.utc)
            road_block.save()
            section = Section.objects.get(id=data.get("id"))
            section.roadblock = False
            section.save()
            return HttpResponse("Road unblocked",status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except Section.DoesNotExist:
        return HttpResponse("Section doesn't exist",status=status.HTTP_404_NOT_FOUND)
    except Blocked.DoesNotExist:
        return HttpResponse("Road isn't blocked",status=status.HTTP_404_NOT_FOUND)

def all_streets(request):
    try:
        if request.method=="GET":
            streets=Street.objects.all()
            return HttpResponse(json.dumps(AllStreetSerializer(streets,many=True).data),status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

def licenses_by_section(request,city):
    try:
        if request.method=="GET":
            section=Section.objects.filter(street__city=city)
            return HttpResponse(json.dumps(LicensesSerializer(section,many=True).data))
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

def charts(request,type,street,begin,end):
    try:
        if request.method=="GET":
            dates=[]
            ammount=[]
            begin=begin.split("-")
            end=end.split("-")
            begin_day=datetime(int(begin[0]),int(begin[1]),int(begin[2]),0,0,0)
            end_day=datetime(int(end[0]),int(end[1]),int(end[2]),0,0,0)
            difference_days=(end_day-begin_day).days
            if type == "accident":
                for i in range(difference_days):
                        temp_day=begin_day+timedelta(days=i)
                        dates.append(f"{temp_day.year}-{temp_day.month}-{temp_day.day}")
                        ammount.append(len(Accident.objects.filter(date__year=temp_day.year, date__month=temp_day.month, date__day=temp_day.day,section__street=street)))
            elif type == "roadblock":
                for i in range(difference_days):
                        temp_day=begin_day+timedelta(days=i)
                        dates.append(f"{temp_day.year}-{temp_day.month}-{temp_day.day}")
                        vals=Blocked.objects.filter(begin__lt=temp_day,section__street=street)
                        if len(vals):
                            for j in vals:
                                print(j.end)
                                if j.end is None:
                                    ammount.append(1)
                                elif j.end.replace(tzinfo=None)>temp_day:
                                    ammount.append(1)
                                else:
                                    ammount.append(0)
                        else:
                            ammount.append(0)

            return HttpResponse(json.dumps({"Days":dates,"ammount":ammount}),status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

def available_cities(request):
    try:
        if request.method=="GET":
            final=list(set([street.city for street in Street.objects.all().only("city")]))
            return HttpResponse(json.dumps(final), status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

