
from decimal import Decimal
from rest_framework import serializers
from band.models import BandPackage, AdditionalService, AvailableService, FreshowsProfile, Member, Client, MusicDirector, Calender, Contract, ClientPerformanceDetail, ServiceOrdering, FinalServiceOrderApproval, Review


class FreshowsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreshowsProfile
        fields = ['id', 'freshows_logo', 'slogan',  'description']


class ClientSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField( read_only =True) 
 
    class Meta:
        model = Client
        fields = ['id', 'user_id', 'phone', 'email', 'detailed_occupation']
    
    def create(self, validated_data):
        user_id = self.context['request'].user.id
        if Client.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError("A client with this user already exists.")
        validated_data['user_id'] = user_id
        return super().create(validated_data)
    
class MemberSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)   


    class Meta:
        model = Member
        fields = ['id', 'user_id', 'artistic_name', 'phone', 'email', 'detailed_Band_Role']
    
    def create(self, validated_data):
        user_id = self.context['request'].user.id
        if Member.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError("A member with this user already exists.")
        validated_data['user_id'] = user_id
        return super().create(validated_data)
    
class MusicDirectorSerializer(serializers.ModelSerializer): 
    class Meta:
        model = MusicDirector
        fields = ['id', 'notifications', 'sound_check_date', 'perfomance_date', 'band_perfomance_details',\
                  'reference_links', 'reference_images', 'reference_folders', 'assigned_to', 'update_at']
        
      
class CalenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calender
        fields = ['id', 'current_date', 'music_director']
    

class ContractSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Contract
        fields = ['id', 'title', 'description', 'document', 'member']
 

class BandPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandPackage
        fields = ['id', 'title', 'description', 'package_price']
  

class AdditionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalService
        fields = ['id', 'user_id','title', 'issuing_client', 'description', 'created_at', 'updated_at']   


class ClientPerformanceDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField( read_only =True) 

    class Meta:
        model = ClientPerformanceDetail 
        fields = ['id', 'user_id', 'client_issuing', 'show_title', 'description', 'created_at', 'updated_at']


    def create(self, validated_data): 
        user_id = self.context['request'].user.id
        if Member.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError("A member with this user already exists.")
        validated_data['user_id'] = user_id
        return super().create(validated_data)
    
    
class AvailableServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableService
        fields = ['id', 'service_ordering', 'band_package', 'additional_service', 'additional_service_price']



class ServiceOrderingSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()

    class Meta:
        model = ServiceOrdering
        fields = ['id','placed_at', 'client', 'services']

    placed_at = serializers.DateTimeField(read_only= True)
    services = serializers.SerializerMethodField()

    def get_services(self, objects):
        services = objects.services.prefetch_related('band_package', 'additional_service')
        serializer = AvailableServiceSerializer(services, many=True, context=self.context)
        return serializer.data


class FinalServiceOrderApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalServiceOrderApproval
        fields = ['id', 'freshows_logo', 'service_ordered_detail', 'performance_title', 'freshow_phone', 'freshow_email',\
                  'performance_requirements', 'price_breakdown', 'total_price', 'final_approval_status']


class BandPackageReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields= ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        band_package_id = self.context['band_package_id']
        return Review.objects.create(band_package_id= band_package_id, **validated_data)
