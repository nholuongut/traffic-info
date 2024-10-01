from django.db import models
from rest_framework import serializers

'''Start of models'''
class Street(models.Model):
    name=models.CharField(max_length=80)
    begin_coord_x=models.IntegerField()
    begin_coord_y=models.IntegerField()
    ending_coord_x=models.IntegerField()
    ending_coord_y=models.IntegerField()
    city=models.CharField(max_length=80)
    length=models.IntegerField()


class Section(models.Model):
    number_cars=models.IntegerField(default=0)
    # True means left-to-right
    # False means right-to-left
    actual_direction=models.BooleanField()
    # Number of accidents at the moment
    n_accident=models.IntegerField(default=0)
    beginning_coords_x=models.IntegerField()
    ending_coords_x=models.IntegerField()
    beginning_coords_y=models.IntegerField()
    ending_coords_y=models.IntegerField()
    street=models.ForeignKey(Street,on_delete=models.CASCADE)
    connect_to=models.ManyToManyField("self",blank=True)
    visibility=models.IntegerField(default=100)
    roadblock=models.BooleanField(default=False)
    police=models.BooleanField(default=False)
    class Meta:
        unique_together=(('street','beginning_coords_x','beginning_coords_y','actual_direction'),)

class Accident(models.Model):
    coord_x=models.IntegerField()
    coord_y=models.IntegerField()
    section=models.ForeignKey(Section,on_delete=models.CASCADE)
    date=models.DateTimeField()

class Transit(models.Model):
    date=models.DateTimeField()
    section=models.ForeignKey(Section,on_delete=models.CASCADE)

class Blocked(models.Model):
    section=models.ForeignKey(Section,on_delete=models.CASCADE)
    begin=models.DateTimeField()
    end=models.DateTimeField(blank=True,null=True)

class Car(models.Model):
    license_plate=models.CharField(max_length=6,primary_key=True)
    section=models.ForeignKey(Section,on_delete=models.CASCADE)

'''End of models'''

'''Serializables for input'''
class StreetInputSerializer(serializers.ModelSerializer):
    class Meta:
        model=Street
        fields = ('name',
                  'begin_coord_x',
                  'begin_coord_y',
                  'ending_coord_x',
                  'ending_coord_y',
                  'length',
                  'city'
                  )
'''End of serializables for input'''

''' Serializables to send data for roadmap '''
class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Street
        fields = ('name','id',)

class SectionSerializer(serializers.ModelSerializer):
    street=StreetSerializer()
    transit_type=serializers.SerializerMethodField('type')
    def type(self,Section,transit_limit=40):
        if Section.visibility<50:
            transit_limit=16

        if Section.roadblock:
            return 'Blocked'
        elif Section.n_accident>0:
            return 'Congested'
        elif transit_limit<Section.number_cars<2*transit_limit:
            return 'Medium'
        elif Section.number_cars>2*transit_limit:
            return 'Congested'
        else:
            return 'Normal'

    class Meta:
        model = Section
        fields=('id',
                'number_cars',
                'actual_direction',
                'n_accident',
                'beginning_coords_x',
                'beginning_coords_y',
                'ending_coords_x',
                'ending_coords_y',
                'street',
                'transit_type',
                'police',
                'visibility')

''' End of Serializables for Road Map'''

'''Serializables and Cars'''
class SmallSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Section
        fields=('id')
        exclude=['number_cars',
                 'actual_direction',
                 'n_accident',
                 'beginning_coords_x',
                 'beginning_coords_y',
                 'street',
                 'transit_type',
                 'police',
                 'visibility']
class AccidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accident
        fields = ('coord_x',
                'coord_y',
                'date',
                'section')
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model=Car
        fields=('license_plate',
                'section')

''' End Serializables for Accident and Car'''

'''Serializables for Statistics'''
class StreetStatisticsSerializer(serializers.ModelSerializer):
    transit_count=serializers.SerializerMethodField("transit")
    road_block=serializers.SerializerMethodField("blocked")
    total_accident=serializers.SerializerMethodField("accident")
    def transit(self,Street):
        transit_count=self.context.get("transit")
        return len(transit_count)

    def blocked(self,Street):
        roadblocks=self.context.get("blocked")
        total_time=0
        for r in roadblocks:
            total_time+=((r.end-r.begin).seconds)/60
        return {"total_time":total_time,"times":len(roadblocks)}

    def accident(self,Street):
        total_accident=self.context.get("accident")
        return len(AccidentSerializer(total_accident,many=True).data)

    class Meta:
        model=Street
        fields = ('name','transit_count','road_block','total_accident')
'''End of Statistics'''

class AllStreetSerializer(serializers.ModelSerializer):
    key=serializers.IntegerField(source='id')
    value=serializers.CharField(source='name')
    class Meta:
        model=Street
        fields=('key','value')


''' Serializers for Cars In a City '''
class LicensesSerializer(serializers.ModelSerializer):
    licenses=serializers.SerializerMethodField("license_plates")

    def license_plates(self,Section):
        return list(Car.objects.filter(section=Section).values_list("license_plate",flat=True))

    class Meta:
        model=Section
        fields=("id","licenses")

'''End of Serializers for Cars In a City'''

